from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    data = [{
        'nama' : 'Scendy Aprianda I.',
        'pekerjaan' : 'IT Support',
        'pesan' : 'Menerima Uang'
    }]
    return make_response(jsonify({'data' :data}), 200)

@app.route('/karyawan', methods=['GET','POST','PUT','DELETE'])
def karyawan():
    try:
        if request.method == 'GET':
            data = [{
                'nama' : 'Scendy ApriandaI. GET',
                'pekerjaan' : 'IT Support',
                'pesan' : 'Menerima Uang'
            }]
        elif request.method == 'POST':
            data = [{
                'nama' : 'Scendy ApriandaI. POST',
                'pekerjaan' : 'IT Support',
                'pesan' : 'Menerima Uang'
            }]
        elif request.method == 'PUT':
            data = [{
                'nama' : 'Scendy ApriandaI. PUT',
                'pekerjaan' : 'IT Support',
                'pesan' : 'Menerima Uang'
            }]
        else:
            data = [{
                'nama' : 'Scendy ApriandaI. DELETE',
                'pekerjaan' : 'IT Support',
                'pesan' : 'Menerima Uang'
            }]
    except Exception as e:
        return make_response(jsonify({'error' : str(e)}), 400)
    return make_response(jsonify({'data' :data}), 200)

if __name__ == '__main__':
    app.run(debug=True)