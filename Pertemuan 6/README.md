# CRUD Flask dengan Upload File

Aplikasi CRUD sederhana pake Flask yang bisa upload file gambar. Lumayan buat belajar backend development.

## Yang Ada di Sini

- `app.py` - File utama Flask dengan semua route
- `templates/` - Folder template HTML
  - `index.html` - Halaman utama daftar produk
  - `add.html` - Form tambah produk
  - `edit.html` - Form edit produk
- `uploads/` - Folder buat simpan file yang diupload

## Fitur

- Tampil semua produk dari database
- Tambah produk baru dengan upload gambar
- Edit produk yang sudah ada
- Hapus produk dengan konfirmasi
- Upload file gambar (jpg, jpeg, png, gif)

## Cara Setup

### 1. Install Dependencies
```bash
pip install flask flask-mysqldb
```

### 2. Setup Database MySQL
Buat database dan tabel:
```sql
CREATE DATABASE crud_upload_db;
USE crud_upload_db;
CREATE TABLE stok (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50),
    nama VARCHAR(100),
    harga INT,
    filename VARCHAR(255)
);
```

### 3. Konfigurasi Database
Edit file `app.py`, sesuaikan konfigurasi MySQL:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password_mysql_anda'
app.config['MYSQL_DB'] = 'crud_upload_db'
```

## Cara Menjalankan

1. Pastikan MySQL sudah jalan
2. Jalankan aplikasi:
```bash
python app.py
```
3. Buka browser ke `http://127.0.0.1:5000`

## Struktur Database

Tabel `stok`:
- `id` - Primary key auto increment
- `kode` - Kode barang
- `nama` - Nama barang
- `harga` - Harga barang
- `filename` - Nama file gambar

## Route yang Tersedia

- `/` - Halaman utama (daftar produk)
- `/add` - Form tambah produk
- `/edit/<kode>` - Form edit produk
- `/delete/<kode>` - Hapus produk
- `/uploads/<filename>` - Akses file gambar

## Yang Dipelogari

- Flask routing dan template rendering
- Database MySQL dengan Flask-MySQLdb
- File upload dan handling
- CRUD operations
- Form validation
- Bootstrap untuk styling

## Catatan

- File gambar disimpan di folder `uploads/`
- Hanya file gambar yang bisa diupload (jpg, jpeg, png, gif)
- Debug mode aktif untuk development
- Database password harus disesuaikan dengan setup MySQL masing-masing

## Troubleshooting

Kalau error connection ke MySQL:
- Pastikan MySQL service jalan
- Cek username dan password di konfigurasi
- Pastikan database sudah dibuat

Kalau error upload file:
- Pastikan folder `uploads/` ada
- Cek permission folder
- Pastikan file yang diupload adalah gambar

Dibuat buat tugas Backend Semester 3.
