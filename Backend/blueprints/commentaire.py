from flask import Blueprint, jsonify, request
from db import query_db
import datetime

commentaire_bp = Blueprint('commentaire', __name__)

@commentaire_bp.route('/Add_comment/', methods=['POST'])
def post_comment():
    # Assurez-vous que la requête contient du JSON
    if not request.is_json:
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()

    # Valider les données reçues
    id_article = data.get('ID_Article')
    id_utilisateur = data.get('ID_Utilisateur')
    contenu = data.get('Contenu')
    
    if not all([id_article, id_utilisateur, contenu]):
        return jsonify({"error": "Données manquantes pour l'ajout du commentaire"}), 400
    
    # Insérer le commentaire dans la base de données
    #  Avoir la date et heure actuelle en france 
    try:
        print(id_article, id_utilisateur, contenu, datetime.datetime.now())
        query_db('INSERT INTO Commentaire (ID_Article, ID_Utilisateur, Contenu, Date_Publication, Active, Modifier, ID_Commentaire) VALUES (?, ?, ?, ?, 1, 0, NULL)',
                (id_article, id_utilisateur, contenu, datetime.datetime.now()))
        return jsonify({"success": "Commentaire ajouté avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commentaire_bp.route('/Get_comments/<int:id_article>', methods=['GET'])
def get_comments(id_article):
    # Récupérer les commentaires de l'article
    comments = query_db("SELECT A.[ID], A.[ID_Article], A.[ID_Utilisateur], A.[Contenu], A.[Date_Publication], A.[Nombre_Likes], B.Nom, A.Active FROM [Wikilense].[dbo].[Commentaire] A inner join  Utilisateur B on B.ID = A.ID_Utilisateur where A.ID_Article = ? and A.Active = 1", id_article)
    return jsonify(comments)

@commentaire_bp.route('/Delete_comment/<int:id_comment>', methods=['DELETE'])
def delete_comment(id_comment):
    # Supprimer le commentaire
    query_db('UPDATE Commentaire SET Active = 0 WHERE ID = ?', id_comment)
    return jsonify({"success": "Commentaire supprimé avec succès"}), 200