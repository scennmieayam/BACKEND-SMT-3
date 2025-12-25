from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    return sqlite3.connect('stokumkm.db')

#Buat tabel
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS barang (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kode TEXT,
            nama TEXT,
            harga INTEGER,
            jumlah INTEGER,
            file TEXT
        )
    """)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# READ
@app.route('/')
def index():
    conn = get_db()
    data = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template('index.html', data=data)

# CREATE
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        gambar = request.files['file']
        filename = gambar.filename
        gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db()
        conn.execute("INSERT INTO barang (kode, nama, harga, jumlah, file) VALUES (?, ?, ?, ?, ?)", (kode, nama, harga, jumlah, filename))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('form.html')

# UPDATE + GANTI FILE
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    barang = conn.execute("SELECT * FROM barang WHERE id=?", (id,)).fetchone()
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        gambar = request.files['gambar']
        filename = barang[5]
        if gambar and gambar.filename != "":
            old_file = os.path.join(app.config['UPLOAD_FOLDER'], barang[5])
            if os.path.exists(old_file):
                os.remove(old_file)
            filename = gambar.filename
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn.execute("UPDATE barang SET kode=?, nama=?, harga=?, jumlah=?, file=? WHERE id=?", (kode, nama, harga, jumlah, filename, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('form.html', barang=barang)

# DELETE
@app.route('/hapus/<int:id>')
def hapus(id):
    conn = get_db()
    barang = conn.execute("SELECT file FROM barang WHERE id=?", (id,)).fetchone()
    if barang:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], barang[0])
        if os.path.exists(filepath):
            os.remove(filepath)
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)