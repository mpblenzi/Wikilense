from flask import Blueprint, request, jsonify
from db import query_db, log

commentaire_likes_bp = Blueprint('commentaire_likes', __name__)

@commentaire_likes_bp.route('/like_comment/<int:id_comment>', methods=['POST'])
def like_comment(id_comment):
    if not request.is_json:
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()
    id_utilisateur = data.get('ID_Utilisateur')

    if not id_utilisateur:
        return jsonify({"error": "ID_Utilisateur manquant"}), 400

    # Vérifier si l'utilisateur a déjà aimé ce commentaire
    already_liked = query_db('SELECT COUNT(*)  as \'Like_nbr\' FROM CommentaireLike WHERE ID_Commentaire = ? AND ID_Utilisateur = ?', [id_comment, id_utilisateur], one=True)

    if int(already_liked['Like_nbr']) > 0:
        return jsonify({"error": "Commentaire déjà aimé par cet utilisateur"}), 400

    # Ajouter le like dans la base de données
    try:
        print(id_comment, id_utilisateur)
        query_db('INSERT INTO CommentaireLike (ID_Commentaire, ID_Utilisateur) VALUES (?, ?)', [id_comment, id_utilisateur])
        return jsonify({"success": "Like ajouté avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commentaire_likes_bp.route('/unlike_comment/<int:id_comment>', methods=['POST'])
def unlike_comment(id_comment):
    if not request.is_json:
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()
    id_utilisateur = data.get('ID_Utilisateur')

    if not id_utilisateur:
        return jsonify({"error": "ID_Utilisateur manquant"}), 400

    # Retirer le like de la base de données
    try:
        query_db('DELETE FROM CommentaireLike WHERE ID_Commentaire = ? AND ID_Utilisateur = ?', [id_comment, id_utilisateur])
        return jsonify({"success": "Like retiré avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

