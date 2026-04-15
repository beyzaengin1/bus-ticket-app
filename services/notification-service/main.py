from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(title="Notification Service (Bildirimler)")

# Gönderilecek bildirim modeli
class NotificationRequest(BaseModel):
    user_id: int
    pnr_code: str
    email: str
    phone: str

@app.post("/api/notifications/send")
async def send_notification(notification: NotificationRequest):
    """
    Bilet kesildikten sonra kullanıcıya Email ve SMS gönderim simülasyonu (Mock).
    """
    
    # 1. Gerçekçilik katmak için 1 saniyelik gecikme
    time.sleep(1)
    
    # 2. Terminale (Loglara) sanki mail atıyormuşuz gibi yazdırıyoruz
    print(f"--> [EMAIL GÖNDERİLDİ] Alıcı: {notification.email} | Konu: Biletiniz Onaylandı | PNR: {notification.pnr_code}")
    print(f"--> [SMS GÖNDERİLDİ] Alıcı: {notification.phone} | Mesaj: Sayın yolcumuz, biletiniz kesilmiştir. PNR: {notification.pnr_code}")
    
    return {
        "status": "success",
        "message": "Bildirimler başarıyla kuyruğa eklendi ve gönderildi.",
        "delivered_to": [notification.email, notification.phone]
    }