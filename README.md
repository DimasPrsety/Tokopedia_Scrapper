# Pricing Update on Tokopedia

Project memang belum selesai, dalam rencananya akan dibuat scrapping data Tokopedia 

### Tujuannya
•⁠  ⁠Bisa pinpoint harga berapa di setiap kategori udang / ikan yang lagi trend
•⁠  ⁠⁠Dan apa reviewnya dari setiap produk

### Data
•⁠  ⁠Scraping produk dari search bar sekitar 22 kateogri produk

### Data Flow
- Data Scrapped using selenium dan bs4 (scrapper-extract.py)
- ETL flow diatur oleh Airflow (scrapper-extract.py)
- Penghubung menggunakan docker (Dockerfile & docker-compose.yaml)
- Database akan diarahkan ke SQLlite
- Lalu dibangun dashboard menggunakan streamlit

Problem saat ini
- Baru sampai poin 2, dockerfile dan dag airflow masih diotak atik

Cheers