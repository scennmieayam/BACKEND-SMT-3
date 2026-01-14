from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.utils import secure_filename
import os
import math

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('rupiah')
def rupiah_format(value):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value
    return 'Rp ' + format(int(round(amount)), ',d').replace(',', '.')

def db():
    conn = sqlite3.connect("hotel_database_sqlite")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kamar (
            id_kamar INTEGER PRIMARY KEY AUTOINCREMENT,
            nomor_kamar TEXT NOT NULL,
            tipe_kamar TEXT NOT NULL,
            harga_per_malam REAL NOT NULL,
            status TEXT NOT NULL,
            filename TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    
    conn = db()
    
    if search_query:
        count_result = conn.execute("SELECT COUNT(*) FROM kamar WHERE nomor_kamar LIKE ? OR tipe_kamar LIKE ? OR status LIKE ?", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')).fetchone()
        total_rows = count_result[0]
        rows = conn.execute("""
            SELECT * FROM kamar
            WHERE nomor_kamar LIKE ? OR tipe_kamar LIKE ? OR status LIKE ?
            LIMIT ? OFFSET ?
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', per_page, offset)).fetchall()
    else:
        count_result = conn.execute("SELECT COUNT(*) FROM kamar").fetchone()
        total_rows = count_result[0]
        rows = conn.execute("SELECT * FROM kamar LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    
    total_pages = math.ceil(total_rows / per_page) if per_page > 0 else 1
    conn.close()
    
    return render_template("index.html", kamars=rows, page=page, total_pages=total_pages, search_query=search_query)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nomor_kamar = request.form["nomor_kamar"]
        tipe_kamar = request.form["tipe_kamar"]
        harga_per_malam = request.form["harga_per_malam"]
        status = request.form["status"]
        
        filename = ""
        if 'filename' in request.files:
            file = request.files['filename']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = db()
        conn.execute("INSERT INTO kamar (nomor_kamar, tipe_kamar, harga_per_malam, status, filename) VALUES (?, ?, ?, ?, ?)", (nomor_kamar, tipe_kamar, harga_per_malam, status, filename))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = db()
    stok = conn.execute("SELECT * FROM kamar WHERE id_kamar=?", (id,)).fetchone()
    if request.method == "POST":
        nomor_kamar = request.form["nomor_kamar"]
        tipe_kamar = request.form["tipe_kamar"]
        harga_per_malam = request.form["harga_per_malam"]
        status = request.form["status"]
        
        filename = stok['filename'] if stok['filename'] else ""
        if 'filename' in request.files:
            file = request.files['filename']
            if file and file.filename != '' and allowed_file(file.filename):
                if filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn.execute("UPDATE kamar SET nomor_kamar=?, tipe_kamar=?, harga_per_malam=?, status=?, filename=? WHERE id_kamar=?", (nomor_kamar, tipe_kamar, harga_per_malam, status, filename, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    conn.close()
    return render_template("edit.html", kamars=stok)

@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    conn.execute("DELETE FROM kamar WHERE id_kamar=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

