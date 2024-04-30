from flask import Blueprint, jsonify
from db import query_db, log
from flask import request
import asyncio

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
async def get_subcategories():
    try: 
        subcategories = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
        await log("Récupération des sous-catégories", "info")
        return jsonify(subcategories)
    except Exception as e:
        await log(f"Erreur lors de la récupération des sous-catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/<int:id>', methods=['GET'])
async def get_category(id):
    try: 
        category = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID = ?", id)
        await log(f"Récupération de la catégorie avec l'id {id}", "info")
        return jsonify(category)
    except Exception as e:
        await log(f"Erreur lors de la récupération de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/all', methods=['GET'])
async def get_categorys():
    try :
        categorys = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie]")
        await log("Récupération de toutes les catégories", "info")
        return jsonify(categorys)
    except Exception as e:
        await log(f"Erreur lors de la récupération de toutes les catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/sous_categorie_de_categorie/<int:id>', methods=['GET'])
async def get_sous_categorie_de_categorie(id):
    try: 
        sous_categorie = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", id)
        await log(f"Récupération des sous-catégories de la catégorie avec l'id {id}", "info")
        return jsonify(sous_categorie)
    except Exception as e:
        await log(f"Erreur lors de la récupération des sous-catégories de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/souscategory/by_id', methods=['GET'])
async def get_categories():
    technology_id = request.args.get('technology')
    if technology_id:
        try:
            categories = await query_db('SELECT * FROM Categorie WHERE ID_Categorie_Parent = ?', [technology_id], one=False)
            await log(f"Getting categories for technology {technology_id}", "info")
            return jsonify(categories), 200
        except Exception as e:
            await log(f"Error while getting categories : {e}", "error")
            return jsonify({"error": str(e)}), 500
    else:
        await log("No technology ID provided", "error")
        return jsonify({"error": "No technology ID provided"}), 400
