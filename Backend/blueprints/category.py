from flask import Blueprint, jsonify
from db import query_db
from flask import request

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def get_subcategories():
    subcategories = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
    return jsonify(subcategories)

@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID = ?", id)
    return jsonify(category)

@category_bp.route('/all', methods=['GET'])
def get_categorys():
    categorys = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie]")
    return jsonify(categorys)

@category_bp.route('/sous_categorie_de_categorie/<int:id>', methods=['GET'])
def get_sous_categorie_de_categorie(id):
    sous_categorie = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", id)
    return jsonify(sous_categorie)

@category_bp.route('/souscategory/by_id', methods=['GET'])
def get_categories():
    technology_id = request.args.get('technology')
    print(technology_id)
    if technology_id:
        try:
            categories = query_db('SELECT * FROM Categorie WHERE ID_Categorie_Parent = ?', [technology_id], one=False)
            return jsonify(categories), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "No technology ID provided"}), 400
