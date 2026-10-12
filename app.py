import os
import pymysql
from dotenv import load_dotenv

# 1. Load data dari file .env
load_dotenv()

# 2. Ambil konfigurasi menggunakan os.environ
koneksi = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with koneksi.cursor() as cursor:
        # Query untuk mengambil data (SELECT)
        sql = "SELECT id, nama, email FROM pengguna"
        cursor.execute(sql)

        #  Ambil semua hasil query
        semua_pengguna = cursor.fetchall()

        print("\n--- DATA DARI MARIADB DOCKER ---")
        for pengguna in semua_pengguna:
            print(f"ID: {pengguna['id']} | Nama: {pengguna['nama']} | Email: {pengguna['email']}")
            print("--------------------------------\n")

finally:
    # jangan lupa tutup koneksi jika sudah selesai
    koneksi.close()

