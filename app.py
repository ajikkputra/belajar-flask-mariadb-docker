import os
import pymysql
from flask import Flask, render_template_string, request, redirect, url_for
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

    
     # Template HTML baru yang sudah dilengkapi Form Input
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Belajar Docker + Flask + Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
            h1, h2 { color: #333; }
            form { background: white; padding: 20px; border-radius: 5px; width: 47%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            input[type=text], input[type=email] { width: 90%; padding: 8px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
            input[type=submit] { background-color: #28a745; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
            table { width: 50%; border-collapse: collapse; margin-top: 20px; background: white; }
            th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }
            th { background-color: #007bff; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Aplikasi Pengguna Modern</h1>
        
        <!-- FORM INPUT UNTUK PENGGUNA -->
        <h2>Tambah Pengguna Baru:</h2>
        <form method="POST">
            <label>Nama:</label><br>
            <input type="text" name="nama" placeholder="Masukkan nama..." required><br>
            <label>Email:</label><br>
            <input type="email" name="email" placeholder="Masukkan email..." required><br><br>
            <input type="submit" value="Simpan Ke Database">
        </form>

        <br><hr><br>

        <h2>Daftar Pengguna Aktif (Dari MariaDB Docker):</h2>
        <table>
            <tr><th>ID</th><th>Nama</th><th>Email</th></tr>
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
