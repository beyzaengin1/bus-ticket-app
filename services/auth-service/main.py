from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(title="Auth Service (Kullanıcı İşlemleri)")

# Kullanıcı verilerini tutacağımız geçici mock veritabanı (İçinde hazır 1 test kullanıcısı var)
MOCK_USERS = {
    "test@ornek.com": {"password": "123", "name": "Test Kullanıcı", "id": 1}
}

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/auth/register")
async def register(user: UserRegister):
    """Yeni kullanıcı kaydı yapar"""
    if user.email in MOCK_USERS:
        raise HTTPException(status_code=400, detail="Bu email adresi zaten kayıtlı.")
    
    # Yeni kullanıcıyı mock listeye ekliyoruz
    new_user_id = len(MOCK_USERS) + 1
    MOCK_USERS[user.email] = {
        "password": user.password,
        "name": user.name,
        "id": new_user_id
    }
    
    return {"message": "Kayıt başarılı", "user_id": new_user_id}

@app.post("/api/auth/login")
async def login(user: UserLogin):
    """Kullanıcı girişi yapar ve Token (Güvenlik Anahtarı) verir"""
    db_user = MOCK_USERS.get(user.email)
    
    # Kullanıcı yoksa veya şifre yanlışsa hata ver
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Geçersiz email veya şifre.")
    
    # Başarılı girişte sahte (mock) bir JWT Token üret
    mock_token = f"fake-jwt-token-{uuid.uuid4()}"
    
    return {
        "message": "Giriş başarılı",
        "access_token": mock_token,
        "token_type": "bearer",
        "user": {"id": db_user["id"], "name": db_user["name"]}
    }