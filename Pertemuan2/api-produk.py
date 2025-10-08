from flask import Flask, jsonify

app = Flask(__name__)

# data produk
produk = {
    "snack": [
        {"id": 1, "nama": "Hihang Hoheng", "harga": 12000},
        {"id": 2, "nama": "Lumpia Hoheng", "harga": 8000},
        {"id": 3, "nama": "Mie Ayam Ken", "harga": 12000}
    ],
    "drink": [
        {"id": 1, "nama": "Es Teh Anget", "harga": 5000},
        {"id": 2, "nama": "Jus Kopi", "harga": 5000},
        {"id": 3, "nama": "Kopi Kapal Titanic", "harga": 60000}
    ]
}

# halaman utama
@app.route('/')
def home():
    return "Selamat Datang Di Produk UMKM Hoheng"

# snack
@app.route('/produk/snack', methods=['GET'])
def get_snack():
    return jsonify(produk["snack"])

# drink
@app.route('/produk/drink', methods=['GET'])
def get_drink():
    return jsonify(produk["drink"])

#snack berdasarkan id
@app.route('/produk/snack/<int:snack_id>', methods=['GET'])
def get_snack_by_id(snack_id):
    item = next((s for s in produk["snack"] if s["id"] == snack_id), None)
    if item:
        return jsonify(item)
    return jsonify({"message": "Snack tidak ditemukan"}), 404

#drink berdasarkan id
@app.route('/produk/drink/<int:drink_id>', methods=['GET'])
def get_drink_by_id(drink_id):
    item = next((d for d in produk["drink"] if d["id"] == drink_id), None)
    if item:
        return jsonify(item)
    return jsonify({"message": "Drink tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(debug=True)
