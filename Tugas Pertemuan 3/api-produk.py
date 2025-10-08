from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_produk(file_type):
    if file_type == 'snack':
        with open('BACKEND\Pertemuan3\snacks.json', 'r') as f:
            return json.load(f)
    elif file_type == 'drink':
        with open('BACKEND\Pertemuan3\drinks.json', 'r') as f:
            return json.load(f)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"pesan": "Selamat Datang Di Produk UMKM"})

@app.route('/produk/snack', methods=['GET'])
def get_snacks():
    snacks = load_produk('snack')
    return jsonify({"pesan": "Halaman Produk Semua Snack..", "data": snacks})

@app.route('/produk/drink', methods=['GET'])
def get_drinks():
    drinks = load_produk('drink')
    return jsonify({"pesan": "Halaman Produk Semua Soft Drink..", "data": drinks})

@app.route('/produk/snack/<int:snack_id>', methods=['GET'])
def get_snack_by_id(snack_id):
    snacks = load_produk('snack')
    snack = next((snack for snack in snacks if snack['id'] == snack_id), None)
    if snack:
        return jsonify({"pesan": f"Halaman Produk Snack dengan id = {snack_id}", "data": snack})
    return jsonify({"pesan": "Snack tidak ditemukan"}), 404

@app.route('/produk/drink/<int:drink_id>', methods=['GET'])
def get_drink_by_id(drink_id):
    drinks = load_produk('drink')
    drink = next((drink for drink in drinks if drink['id'] == drink_id), None)
    if drink:
        return jsonify({"pesan": f"Halaman Produk Soft Drink dengan id = {drink_id}", "data": drink})
    return jsonify({"pesan": "Drink tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(debug=True)