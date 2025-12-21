import os
import math
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='static/templates')
Bootstrap(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

client = MongoClient("mongodb://localhost:27017/")
db = client["crud_kamar_hotel"]
collection = db["kamars"]

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    if search_query:
        query = {
            '$or': [
                {'nomor_kamar': {'$regex': search_query, '$options': 'i'}},
                {'tipe_kamar': {'$regex': search_query, '$options': 'i'}}
            ]
        }
    else:
        query = {}

    total_rows = collection.count_documents(query)
    total_pages = math.ceil(total_rows / per_page) if per_page > 0 else 1

    kamar = collection.find(query).skip(offset).limit(per_page)
    return render_template('index.html', kamars=kamar, page=page, total_pages=total_pages, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        nomor_kamar = request.form['nomor_kamar']
        tipe_kamar = request.form['tipe_kamar']
        harga_per_malam = request.form['harga_per_malam']
        status = request.form['status']

        existing = collection.find_one({'nomor_kamar': nomor_kamar})
        if existing:
            return render_template(
                'add.html',
                error='Nomer kamar telah ada',
                nomor_kamar=nomor_kamar,
                tipe_kamar=tipe_kamar,
                harga_per_malam=harga_per_malam,
                status=status
            )

        foto = None
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto = filename
        
        collection.insert_one({
            'nomor_kamar': nomor_kamar,
            'tipe_kamar': tipe_kamar,
            'harga_per_malam': harga_per_malam,
            'status': status,
            'foto': foto
        })
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_file(id):
    kamar = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nomor_kamar = request.form['nomor_kamar']
        tipe_kamar = request.form['tipe_kamar']
        harga_per_malam = request.form['harga_per_malam']
        status = request.form['status']

        existing = collection.find_one({'nomor_kamar': nomor_kamar, '_id': {'$ne': ObjectId(id)}})
        if existing:
            return render_template(
                'edit.html',
                kamar=kamar,
                error='Nomer kamar telah ada'
            )

        foto = kamar.get('foto')
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto = filename
        
        collection.update_one({'_id': ObjectId(id)}, {'$set': {
            'nomor_kamar': nomor_kamar,
            'tipe_kamar': tipe_kamar,
            'harga_per_malam': harga_per_malam,
            'status': status,
            'foto': foto
        }})
        return redirect(url_for('index'))
    return render_template('edit.html', kamar=kamar)

@app.route('/delete/<id>')
def delete_file(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
