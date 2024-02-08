from flask import Blueprint, jsonify
from db import query_db

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def get_subcategories():
    subcategories = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
    data = [{'id': cat[0], 'nom': cat[1], 'path': cat[2]} for cat in subcategories]
    return jsonify(data)

@category_bp.route('/all', methods=['GET'])
def get_categorys():
    categorys = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie]")
    data = [{'id': cat[0], 'nom': cat[1], 'path': cat[2]} for cat in categorys]
    return jsonify(data)

@category_bp.route('/sous_categorie_de_categorie/<int:id>', methods=['GET'])
def get_sous_categorie_de_categorie(id):
    sous_categorie = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", id)
    data = [{'id': cat[0], 'nom': cat[1], 'path': cat[2]} for cat in sous_categorie]
    return jsonify(data)