from fastapi import FastAPI, Request
import time

# 1. API Gateway Uygulamamızı Başlatıyoruz
app = FastAPI(title="Bus Ticket API Gateway", version="1.0.0")

# 2. HOCANIN İSTEDİĞİ MIDDLEWARE YAPISI
# Gelen her istek önce bu fonksiyona çarpar.
@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    start_time = time.time()
    
    # İSTEK GELDİĞİNDE: Burada loglama veya güvenlik (Auth) kontrolü yapılabilir.
    print(f"--> [GATEWAY] Gelen İstek: {request.method} {request.url}")
    
    # İsteği ilgili mikroservise ilet (Şu an kendi içinde işliyor)
    response = await call_next(request)
    
    # CEVAP DÖNERKEN: İşlem süresini hesapla
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"<-- [GATEWAY] Cevap Döndü. İşlem Süresi: {process_time:.4f} saniye")
    
    return response

# 3. Test İçin Ana Rota
@app.get("/")
async def root():
    return {"mesaj": "API Gateway Aktif! Tüm trafik başarılı bir şekilde buradan geçiyor."}