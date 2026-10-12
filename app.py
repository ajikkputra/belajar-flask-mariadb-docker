import os
import pymysql
from flask import Flask, render_template_string
from dotenv import load_dotenv

# 1. Inisialisasi Flask dan Load .env
app = Flask(__name__)
load_dotenv()

# Fungsi bantuan untuk mengambil data dari MariaDB Docker
def ambil_data_database():
    # Konfigurasi koneksi ke MariaDB Docker Anda
    koneksi = pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with koneksi.cursor() as cursor:
            cursor.execute("SELECT id, nama, email FROM pengguna")
            return cursor.fetchall()
    finally:
        koneksi.close()

# 2. Membuat Rute Utama Website (Route)
@app.route('/')
def home():
    data_pengguna = ambil_data_database()
    
    # Template HTML sederhana langsung di dalam kode Python (sementara agar praktis)
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Belajar Docker + Flask</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
            h1 { color: #333; }
            table { width: 50%; border-collapse: collapse; margin-top: 20px; background: white; }
            th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }
            th { background-color: #007bff; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Daftar Pengguna dari MariaDB Docker</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Nama</th>
                <th>Email</th>
            </tr>
            {% for user in pengguna %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.nama }}</td>
                <td>{{ user.email }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, pengguna=data_pengguna)

# 3. Menjalankan Aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
