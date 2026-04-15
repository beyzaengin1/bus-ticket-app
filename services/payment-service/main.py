from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI(title="Payment Service (Mock)")

# Kullanıcıdan gelecek ödeme bilgilerinin modeli
class PaymentRequest(BaseModel):
    user_id: int
    trip_id: int
    card_number: str
    amount: float

@app.post("/api/payment/process")
async def process_payment(payment_data: PaymentRequest):
    """
    MOCK ÖDEME SİMÜLASYONU: Gerçek bir bankaya gitmez, senaryo üretir.
    Hocanın görmek istediği 'Mock' deneyimi tam olarak burasıdır.
    """
    
    # 1. Gerçekçilik katmak için 1-3 saniye arası sahte bir bekleme süresi (Bankaya bağlanıyormuş gibi)
    time.sleep(random.uniform(1.0, 3.0))
    
    # 2. MOCK SENARYOLARI
    # Senaryo A: Eğer kart numarası '0000' ile bitiyorsa 'Bakiye Yetersiz' hatası ver (Test için)
    if payment_data.card_number.endswith("0000"):
        raise HTTPException(status_code=400, detail="Ödeme Başarısız: Yetersiz Bakiye veya Geçersiz Kart.")
    
    # Senaryo B: Eğer kart numarası '9999' ile bitiyorsa 'Sistem Hatası' ver
    if payment_data.card_number.endswith("9999"):
        raise HTTPException(status_code=500, detail="Banka sistemlerinde anlık bir kesinti yaşandı.")

    # Senaryo C: Diğer tüm durumlarda ödeme başarılı sayılır.
    mock_transaction_id = f"TXN-{random.randint(100000, 999999)}"
    
    return {
        "status": "success",
        "message": "Ödeme başarıyla alındı.",
        "transaction_id": mock_transaction_id,
        "amount_paid": payment_data.amount
    }