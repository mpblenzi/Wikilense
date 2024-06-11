from flask import Blueprint, request, jsonify
from utils.db import query_db, log
import asyncio

commentaire_likes_bp = Blueprint('commentaire_likes', __name__)

@commentaire_likes_bp.route('/like_comment/<int:id_comment>', methods=['POST'])
async def like_comment(id_comment):
    if not request.is_json:
        await log("La requête doit être en JSON", "error")
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()
    id_utilisateur = data.get('ID_Utilisateur')
    # Ajouter le like dans la base de données    
    if not id_utilisateur:
        await log("ID_Utilisateur manquant", "error")
        return jsonify({"error": "ID_Utilisateur manquant"}), 400

    # Vérifier si l'utilisateur a déjà aimé ce commentaire
    already_liked = await query_db('SELECT COUNT(*)  as \'Like_nbr\' FROM CommentaireLike WHERE ID_Commentaire = ? AND ID_Utilisateur = ?', [id_comment, id_utilisateur], one=True)
    if int(already_liked['Like_nbr']) > 0:
        await log("Commentaire déjà aimé par cet utilisateur", "error")
        return jsonify({"error": "Commentaire déjà aimé par cet utilisateur"}), 400
    
    try:
        await query_db('INSERT INTO CommentaireLike (ID_Commentaire, ID_Utilisateur) VALUES (?, ?)', [id_comment, id_utilisateur])
        await log("Like ajouté avec succès", "success")
        return jsonify({"success": "Like ajouté avec succès"}), 200
    except Exception as e:
        await log(f"Erreur lors de l'ajout du like : {e}", "error")
        return jsonify({"error": str(e)}), 500

@commentaire_likes_bp.route('/unlike_comment/<int:id_comment>', methods=['POST'])
async def unlike_comment(id_comment):
    if not request.is_json:
        await log("La requête doit être en JSON", "error")
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()
    id_utilisateur = data.get('ID_Utilisateur')
    
    print(id_utilisateur)
    if not id_utilisateur:
        await log("ID_Utilisateur manquant", "error")
        return jsonify({"error": "ID_Utilisateur manquant"}), 400

    # Retirer le like de la base de données
    try: 
        await query_db('DELETE FROM CommentaireLike WHERE ID_Commentaire = ? AND ID_Utilisateur = ?', [id_comment, id_utilisateur])
        await log("Like retiré avec succès", "success")
        return jsonify({"success": "Like retiré avec succès"}), 200
    except Exception as e:
        await log(f"Erreur lors du retrait du like : {e}", "error")
        return jsonify({"error": str(e)}), 500

@commentaire_likes_bp.route('/get_likes_count/<int:id_comment>', methods=['GET'])
async def get_likes_count(id_comment):
    await log("Récupération du nombre de likes", "info")
    likes_count = await query_db('SELECT COUNT(*) as \'Likes\' FROM CommentaireLike WHERE ID_Commentaire = ?', [id_comment], one=True)
    return likes_count['Likes']

#verifier le nombre de like sur un commentaire
@commentaire_likes_bp.route('/check_like/<int:id_comment>', methods=['GET'])
async def check_like(id_comment):
    # Vérifier si l'utilisateur a déjà aimé ce commentaire
    already_liked = await query_db('SELECT Count(*) as \'Nbr_like\' FROM [Wikilense].[dbo].[Commentaire] A inner join [Wikilense].[dbo].[CommentaireLike] B on A.ID = B.ID_Commentaire where A.ID = ?', [id_comment], one=True)
    return already_liked

# Vérifier si l'utilisateur a déjà aimé ce commentaire
@commentaire_likes_bp.route('/check_like_user/<int:id_comment>', methods=['GET'])
async def check_like_user(id_comment):
    id_utilisateur = request.args.get('ID_Utilisateur')
    
    if id_utilisateur is None:
        return jsonify({"error": "ID_Utilisateur manquant"}), 400
    
    print(id_utilisateur)
    print(id_comment)

    already_liked = await query_db('SELECT COUNT(*) as \'Like_nbr\' FROM CommentaireLike WHERE ID_Commentaire = ? AND ID_Utilisateur = ?', [id_comment, id_utilisateur], one=True)
    
    print(already_liked)
    
    if int(already_liked['Like_nbr']) > 0:
        already_liked = True
    else:
        already_liked = False
    
    return jsonify({"is_liked_by_current_user": already_liked})