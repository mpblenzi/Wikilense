from flask import Blueprint, jsonify
from db import query_db

article_bp = Blueprint('article', __name__)

@article_bp.route('/by_categorie/<int:id_category>', methods=['GET'])
def get_article_by_category(id_category):
    articles = query_db('SELECT * FROM Article WHERE [ID_Sous_Sous_Categorie] = ?', [id_category])
    return jsonify(articles)

@article_bp.route('/by_id/<int:id_article>', methods=['GET'])
def get_article_by_id(id_article):
    article = query_db('  SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [id_article])
    return jsonify(article)