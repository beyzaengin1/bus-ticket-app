from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI(title="Booking Service (Bilet Satın Alma)")

# Kullanıcıdan gelecek rezervasyon/satın alma isteği
class BookingRequest(BaseModel):
    user_id: int
    trip_id: int
    seat_number: int
    card_number: str

@app.post("/api/bookings/create")
async def create_booking(booking: BookingRequest):
    """
    Bilet satın alma işlemini başlatır. 
    Gerçek mimaride burada Payment ve Trip servisleri ile haberleşilir.
    """
    
    # 1. KONTROL: Koltuk numarası mantıklı mı? (Mock kontrol)
    if booking.seat_number <= 0 or booking.seat_number > 40:
        raise HTTPException(status_code=400, detail="Geçersiz koltuk numarası. Lütfen 1-40 arası seçin.")
    
    # 2. ÖDEME SİMÜLASYONU: Ödeme servisiyle konuşuyormuş gibi yapıyoruz.
    # Hatırlarsan Payment servisinde sonu 0000 olanlara ret vermiştik. Aynı mantığı burada da kurguluyoruz.
    time.sleep(1) # İşlem yapılıyormuş hissi
    if booking.card_number.endswith("0000"):
        raise HTTPException(status_code=400, detail="Bilet Alınamadı: Ödeme reddedildi (Yetersiz Bakiye).")

    # 3. BAŞARILI BİLETLEME (PNR Kodu Üretimi)
    # Eğer buraya kadar hata fırlatılmadıysa bilet kesilir.
    pnr_code = f"PNR-{random.randint(100000, 999999)}"
    
    # İleride tam bu noktada Kafka'ya "Bilet Kesildi, Bildirim Gönder" mesajı atılacak.
    
    return {
        "status": "success",
        "message": "Harika! Biletiniz başarıyla oluşturuldu.",
        "pnr_code": pnr_code,
        "trip_details": {
            "trip_id": booking.trip_id,
            "seat": booking.seat_number
        }
    }