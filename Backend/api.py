from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, send_from_directory
import pyodbc

app = Flask(__name__)
CORS(app)


server = 'AZFRCER0300\DWK1' 
database = 'Wikilense' 
username = 'Wikilense' 
password = 'Qgx8NdQk5UKn49cKUVHgBfAd4nqeKZW6EbzkRjxS495ZDNhJw7' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+
                    server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

@app.route('/data/category', methods=['GET'])
def get_data():
    cursor.execute("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(list(row))
    return jsonify(data)

@app.route('/images_category/<filename>')
def serve_image_category(filename):
    return send_from_directory('asset/category/', filename)

@app.route('/data/sous-category/<id>', methods=['GET'])
def get_sous_category(id):
    cursor.execute("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", id)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append(list(row))
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
