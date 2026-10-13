# 🚀 Aplikasi Flask-MariaDB Modern dengan Docker

Proyek ini adalah aplikasi web backend berbasis **Python Flask** yang terhubung secara real-time ke database **MariaDB** yang berjalan di dalam lingkungan terisolasi **Docker Container**. Proyek ini dirancang menggunakan arsitektur folder standar industri.

## 🛠️ Tech Stack yang Digunakan
* **Infrastruktur:** [Docker](https://docker.com) (MariaDB Container)
* **Backend Framework:** [Flask (Micro-framework)](https://palletsprojects.com)
* **Database Driver:** PyMySQL
* **Database Management GUI:** DBeaver / Docker CLI
* **Environment Management:** python-dotenv & venv

## 📂 Struktur Proyek
```text
├── env/                 # Virtual environment Python (diabaikan oleh Git)
├── static/              # Tempat file aset statis (CSS)
│   └── style.css
├── templates/           # Tempat file template HTML
│   └── index.html
├── .env                 # Konfigurasi rahasia database (diabaikan oleh Git)
├── .gitignore           # Satpam penyaring berkas Git
├── app.py               # Kode utama Flask Backend & Router API
└── README.md            # Dokumentasi proyek
```

## ⚙️ Cara Menjalankan Proyek Secara Lokal

### 1. Jalankan Database MariaDB di Docker
Pastikan Docker Desktop Anda sudah aktif, lalu jalankan container MariaDB dengan perintah berikut:
```bash
docker run --name mariadb-belajar -e MARIADB_ROOT_PASSWORD=rahasia123 -p 3306:3306 -v mariadb_data:/var/lib/mysql -d mariadb:latest
```
*(Atau jalankan `docker start mariadb-belajar` jika container sudah pernah dibuat).*

### 2. Buat File Konfigurasi `.env`
Buat file bernama `.env` di folder utama proyek dan masukkan kredensial berikut:
```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=rahasia123
DB_NAME=belajar_docker
```

### 3. Aktifkan Virtual Environment & Jalankan Flask
```bash
# Aktifkan venv Anda (sesuaikan dengan OS Anda)
# Windows (CMD): env\Scripts\activate

# Jalankan server
python app.py
```
Buka browser Anda dan akses `http://localhost:5000` atau cek API murni di `http://localhost:5000/api/pengguna`.
