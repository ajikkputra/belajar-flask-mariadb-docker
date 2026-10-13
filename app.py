import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from flask import jsonify

# 1. Inisialisasi Flask dan Load .env
app = Flask(__name__)
load_dotenv()

# Fungsi untuk koneksi database
def dapatkan_koneksi():
    # Konfigurasi koneksi ke MariaDB Docker Anda
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

# 2. Membuat Rute Utama Website (kita tampilkan data + inputan ya)
@app.route('/', methods=['GET', 'POST'])
def home():
    koneksi = dapatkan_koneksi()

    # 1. jika pengguna menekan tombol kirim (proses tambah data)
    if request.method == 'POST':
        nama_baru = request.form.get('nama')
        email_baru = request.form.get('email')

        try:
            with koneksi.cursor() as cursor:
                # query INSERT otomatis dari input web
                sql = "INSERT INTO pengguna (nama, email) VALUES (%s, %s)"
                cursor.execute(sql, (nama_baru, email_baru))
            koneksi.commit() # mengunci perubahan ke mariaDB docker
        finally:
            koneksi.close()

        return redirect(url_for('home')) # refresh halaman setelah sukses

    # 2. Jika pengguna hanya membuka halaman (menampilkan data aja)
    try:
        with koneksi.cursor() as cursor:
            cursor.execute("SELECT id, nama, email FROM pengguna")
            data_pengguna = cursor.fetchall()
    finally:
        koneksi.close()

    # html_template = 'index.html' ngga perlu buat variable

    return render_template('index.html', pengguna=data_pengguna)

@app.route('/api/pengguna')
def api_pengguna():
    koneksi = dapatkan_koneksi()
    try:
        with koneksi.cursor() as cursor:
            cursor.execute("SELECT id, nama, email FROM pengguna")
            data_pengguna = cursor.fetchall()

        return jsonify(data_pengguna)
    finally:
        koneksi.close()

# 3. Menjalankan Aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
