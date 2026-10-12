import pymysql

# konfigurasi koneksi ke MariaDB Docker
koneksi = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='rahasia',
    database='belajar_docker',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with koneksi.cursor() as cursor:
        # 2. Query untuk mengambil data (SELECT)
        sql = "SELECT id, nama, email FROM pengguna"
        cursor.execute(sql)

        # 3. Ambil semua hasil query
        semua_pengguna = cursor.fetchall()

        print("\n--- DATA DARI MARIADB DOCKER ---")
        for pengguna in semua_pengguna:
            print(f"ID: {pengguna['id']} | Nama: {pengguna['nama']} | Email: {pengguna['email']}")
            print("--------------------------------\n")

finally:
    # jangan lupa tutup koneksi jika sudah selesai
    koneksi.close()

