from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import math

app = Flask(__name__)
app.secret_key = 'secret123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'scendy1904'
app.config['MYSQL_DB'] = 'crud_kamar_hotel'

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

mysql = MySQL(app)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.template_filter('rupiah')
def rupiah_format(value):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value
    #format rupiah tanpa desimal
    return ('Rp ' + format(int(round(amount)), ',')).replace(',', '.')
@app.route('/')
def index():
	search_query = request.args.get('search', '')
	page = int(request.args.get('page', 1))
	per_page = 5
	offset = (page - 1) * per_page

	cur = mysql.connection.cursor()
	if search_query:
		cur.execute("SELECT COUNT(*) FROM kamar WHERE nomor_kamar LIKE %s OR tipe_kamar LIKE %s", ('%' + search_query + '%', '%' + search_query + '%'))
	else:
		cur.execute("SELECT COUNT(*) FROM kamar")
	total_rows = cur.fetchone()[0]
	total_pages = math.ceil(total_rows / per_page) if per_page > 0 else 1

	if search_query:
		cur.execute("""
			SELECT * FROM kamar
			WHERE nomor_kamar LIKE %s OR tipe_kamar LIKE %s
			LIMIT %s OFFSET %s
		""", ('%' + search_query + '%', '%' + search_query + '%', per_page, offset))
	else:
		cur.execute("SELECT * FROM kamar LIMIT %s OFFSET %s", (per_page, offset))

	kamar_list = cur.fetchall()
	cur.close()
	return render_template('index.html', kamars=kamar_list, page=page, total_pages=total_pages, search_query=search_query)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/add', methods=['GET','POST'])
def add_file():
	if request.method == 'POST':
		nomor_kamar = request.form['nomor_kamar']
		tipe_kamar = request.form['tipe_kamar']
		harga_per_malam = request.form['harga_per_malam']
		status = request.form['status']
		file = request.files.get('file')

		filename = None
		if file and file.filename and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO kamar (nomor_kamar, tipe_kamar, harga_per_malam, status, filename) VALUES (%s, %s, %s, %s, %s)", (nomor_kamar, tipe_kamar, harga_per_malam, status, filename))
		mysql.connection.commit()
		cur.close()

		return redirect(url_for('index'))

	return render_template('add.html')

@app.route('/edit/<id>', methods=['GET','POST'])
def edit_file(id):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM kamar WHERE id_kamar = %s", (id,))
	kamar_data = cur.fetchone()

	if request.method == 'POST':
		nomor_kamar = request.form['nomor_kamar']
		tipe_kamar = request.form['tipe_kamar']
		harga_per_malam = request.form['harga_per_malam']
		status = request.form['status']

		new_file = request.files.get('file')
		filename = kamar_data[5] if len(kamar_data) > 5 else None
		if new_file and new_file.filename and allowed_file(new_file.filename):
			filename = secure_filename(new_file.filename)
			os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
			new_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		cur.execute("UPDATE kamar SET nomor_kamar = %s, tipe_kamar = %s, harga_per_malam = %s, status = %s, filename = %s WHERE id_kamar = %s", (nomor_kamar, tipe_kamar, harga_per_malam, status, filename, id))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('index'))

	cur.close()
	return render_template('edit.html', kamar_data=kamar_data)


@app.route('/delete/<id>')
def delete_file(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM kamar WHERE id_kamar = %s", (id,))
	mysql.connection.commit()
	cur.close()
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)