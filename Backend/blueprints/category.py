from flask import Blueprint, jsonify
from db import query_db, log
from flask import request

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def get_subcategories():
    
    try: 
        subcategories = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
        log("Récupération des sous-catégories", "info")
        return jsonify(subcategories)
    except Exception as e:
        log(f"Erreur lors de la récupération des sous-catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    try: 
        category = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID = ?", id)
        log(f"Récupération de la catégorie avec l'id {id}", "info")
        return jsonify(category)
    except Exception as e:
        log(f"Erreur lors de la récupération de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/all', methods=['GET'])
def get_categorys():
    try :
        categorys = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie]")
        log("Récupération de toutes les catégories", "info")
        return jsonify(categorys)
    except Exception as e:
        log(f"Erreur lors de la récupération de toutes les catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/sous_categorie_de_categorie/<int:id>', methods=['GET'])
def get_sous_categorie_de_categorie(id):
    try: 
        sous_categorie = query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", id)
        log(f"Récupération des sous-catégories de la catégorie avec l'id {id}", "info")
        return jsonify(sous_categorie)
    except Exception as e:
        log(f"Erreur lors de la récupération des sous-catégories de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/souscategory/by_id', methods=['GET'])
def get_categories():
    technology_id = request.args.get('technology')
    if technology_id:
        try:
            categories = query_db('SELECT * FROM Categorie WHERE ID_Categorie_Parent = ?', [technology_id], one=False)
            log(f"Getting categories for technology {technology_id}", "info")
            return jsonify(categories), 200
        except Exception as e:
            log(f"Error while getting categories : {e}", "error")
            return jsonify({"error": str(e)}), 500
    else:
        log("No technology ID provided", "error")
        return jsonify({"error": "No technology ID provided"}), 400
