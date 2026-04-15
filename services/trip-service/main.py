from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Trip Service (Seferler)")

# Otobüs Seferi Modeli
class Trip(BaseModel):
    id: int
    departure_city: str
    arrival_city: str
    departure_time: str
    price: float
    available_seats: int

# Geçici Veritabanı (İleride PostgreSQL'e dönüşecek)
MOCK_TRIPS = [
    {"id": 101, "departure_city": "İstanbul", "arrival_city": "Ankara", "departure_time": "2024-05-20 08:00", "price": 450.0, "available_seats": 40},
    {"id": 102, "departure_city": "İstanbul", "arrival_city": "İzmir", "departure_time": "2024-05-20 09:30", "price": 500.0, "available_seats": 12},
    {"id": 103, "departure_city": "Ankara", "arrival_city": "Antalya", "departure_time": "2024-05-21 22:00", "price": 600.0, "available_seats": 5},
]

@app.get("/api/trips", response_model=List[Trip])
async def get_all_trips():
    """Tüm seferleri listeler"""
    return MOCK_TRIPS

@app.get("/api/trips/search", response_model=List[Trip])
async def search_trips(
    departure: str = Query(..., description="Kalkış Şehri"), 
    arrival: str = Query(..., description="Varış Şehri")
):
    """Kalkış ve varış şehrine göre sefer arar"""
    results = [
        trip for trip in MOCK_TRIPS 
        if trip["departure_city"].lower() == departure.lower() 
        and trip["arrival_city"].lower() == arrival.lower()
    ]
    
    if not results:
        raise HTTPException(status_code=404, detail="Bu güzergahta sefer bulunamadı.")
    
    return results