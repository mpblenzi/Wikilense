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
    # Récupérer tous les commentaires et réponses actifs pour l'article
    all_comments = query_db("""
        SELECT 
            A.[ID], A.[ID_Article], A.[ID_Utilisateur], A.[Contenu], 
            A.[Date_Publication], A.[Nombre_Likes], B.Nom, A.Active, 
            A.Modifier, A.[ID_Commentaire]
        FROM [Wikilense].[dbo].[Commentaire] A 
        INNER JOIN Utilisateur B ON B.ID = A.ID_Utilisateur 
        WHERE A.ID_Article = ? AND A.Active = 1
    """, (id_article,))

    # Créer un dictionnaire pour mapper les commentaires avec leurs réponses
    comments_map = {comment['ID']: comment for comment in all_comments}
    for comment in all_comments:
        comment['Reponses'] = []  # Initialiser la liste des réponses

    # Construire la structure de données en imbriquant les réponses
    structured_comments = []
    for comment in all_comments:
        if comment['ID_Commentaire']:  # Si c'est une réponse à un commentaire
            parent_id = comment['ID_Commentaire']
            if parent_id in comments_map:
                # Ajouter la réponse à la liste de son commentaire parent
                comments_map[parent_id]['Reponses'].append(comment)
        else:
            # Si ce n'est pas une réponse, c'est un commentaire principal
            structured_comments.append(comment)

    # Ne renvoyer que les commentaires principaux (ceux sans ID_Commentaire)
    top_level_comments = [comment for comment in structured_comments if comment['ID_Commentaire'] is None]
    return jsonify(top_level_comments)

@commentaire_bp.route('/Delete_comment/<int:id_comment>', methods=['DELETE'])
def delete_comment(id_comment):
    # Supprimer le commentaire
    query_db('UPDATE Commentaire SET Active = 0 WHERE ID = ?', id_comment)
    return jsonify({"success": "Commentaire supprimé avec succès"}), 200

@commentaire_bp.route('/edit/<int:id_comment>', methods=['PUT'])
def edit_comment(id_comment):
    # Assurez-vous que la requête contient du JSON
    if not request.is_json:
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()

    # Valider les données reçues
    print(data)
    contenu = data.get('content')
    
    if not contenu:
        return jsonify({"error": "Données manquantes pour la modification du commentaire"}), 401
    
    # Insérer le commentaire dans la base de données mettre le champ modifier à 1 et le champ Modifier a 1
    try:
        query_db('UPDATE Commentaire SET Contenu = ?, Modifier = 1 WHERE ID = ?', (contenu, id_comment))
        return jsonify({"success": "Commentaire modifié avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@commentaire_bp.route('/Add_comment_reply/', methods=['POST'])
def post_comment_reply():
    # Assurez-vous que la requête contient du JSON
    if not request.is_json:
        return jsonify({"error": "La requête doit être en JSON"}), 400

    data = request.get_json()

    # Valider les données reçues
    id_article = data.get('ID_Article')
    id_utilisateur = data.get('ID_Utilisateur')
    contenu = data.get('Contenu')
    id_article_reply = data.get('ID_Article_Reply')
    
    if not all([id_article, id_utilisateur, contenu]):
        return jsonify({"error": "Données manquantes pour l'ajout du commentaire"}), 400
    
    # Insérer le commentaire dans la base de données
    try:
        print(id_article, id_utilisateur, contenu, datetime.datetime.now())
        query_db('INSERT INTO Commentaire (ID_Article, ID_Utilisateur, Contenu, Date_Publication, Active, Modifier, ID_Commentaire) VALUES (?, ?, ?, ?, 1, 0, ?)',
                (id_article, id_utilisateur, contenu, datetime.datetime.now(), id_article_reply))
        return jsonify({"success": "Commentaire ajouté avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500