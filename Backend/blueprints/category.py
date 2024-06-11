from flask import Blueprint, jsonify, request
from utils.db import query_db, log

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
async def get_subcategories():
    """Récupère toutes les sous-catégories principales."""
    try:
        subcategories = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent IS NULL")
        await log("Récupération des sous-catégories", "info")
        return jsonify(subcategories)
    except Exception as e:
        await log(f"Erreur lors de la récupération des sous-catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/<int:id>', methods=['GET'])
async def get_category(id):
    """Récupère une catégorie spécifique par ID."""
    try:
        category = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID = ?", [id])
        if not category:
            await log(f"Aucune catégorie trouvée avec l'id {id}", "error")
            return jsonify({"error": "Catégorie non trouvée"}), 404
        await log(f"Récupération de la catégorie avec l'id {id}", "info")
        return jsonify(category)
    except Exception as e:
        await log(f"Erreur lors de la récupération de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/all', methods=['GET'])
async def get_categories():
    """Récupère toutes les catégories."""
    try:
        categories = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie]")
        await log("Récupération de toutes les catégories", "info")
        return jsonify(categories)
    except Exception as e:
        await log(f"Erreur lors de la récupération de toutes les catégories : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/sous_categorie_de_categorie/<int:id>', methods=['GET'])
async def get_sous_categorie_de_categorie(id):
    """Récupère les sous-catégories d'une catégorie spécifique."""
    try:
        sous_categories = await query_db("SELECT * FROM [Wikilense].[dbo].[Categorie] WHERE ID_Categorie_Parent = ?", [id])
        if not sous_categories:
            await log(f"Aucune sous-catégorie trouvée pour la catégorie avec l'id {id}", "error")
            return jsonify({"error": "Sous-catégorie non trouvée"}), 404
        await log(f"Récupération des sous-catégories de la catégorie avec l'id {id}", "info")
        return jsonify(sous_categories)
    except Exception as e:
        await log(f"Erreur lors de la récupération des sous-catégories de la catégorie avec l'id {id} : {e}", "error")
        return jsonify({"error": str(e)}), 500

@category_bp.route('/souscategory/by_id', methods=['GET'])
async def get_categories_by_technology():
    """Récupère les catégories basées sur l'ID de la technologie."""
    technology_id = request.args.get('technology')
    if technology_id:
        try:
            categories = await query_db('SELECT * FROM Categorie WHERE ID_Categorie_Parent = ?', [technology_id])
            await log(f"Récupération des catégories pour la technologie {technology_id}", "info")
            return jsonify(categories), 200
        except Exception as e:
            await log(f"Erreur lors de la récupération des catégories : {e}", "error")
            return jsonify({"error": str(e)}), 500
    else:
        await log("Aucun ID de technologie fourni", "error")
        return jsonify({"error": "Aucun ID de technologie fourni"}), 400
