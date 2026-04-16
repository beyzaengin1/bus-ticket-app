# 1. Temel olarak hafif bir Python sürümü al
FROM python:3.11-slim

# 2. Sanal bilgisayarın içinde kendimize bir çalışma klasörü açalım
WORKDIR /app

# 3. İhtiyaç listemizi bu klasöre kopyalayalım
COPY requirements.txt .

# 4. Listede yazan kütüphaneleri indirelim
RUN pip install --no-cache-dir -r requirements.txt

# 5. Projemizdeki tüm kodları sanal bilgisayarın içine kopyalayalım
COPY . .

# (Uygulamayı nasıl başlatacağımızı docker-compose içinde söyleyeceğiz)