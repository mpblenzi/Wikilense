from flask import Blueprint, jsonify
from db import query_db
from flask import request
from werkzeug.utils import secure_filename
import os

article_bp = Blueprint('article', __name__)

@article_bp.route('/by_categorie/<int:id_category>', methods=['GET'])
def get_article_by_category(id_category):
    articles = query_db('SELECT * FROM Article WHERE [ID_Sous_Sous_Categorie] = ?', [id_category])
    return jsonify(articles)

@article_bp.route('/by_id/<int:id_article>', methods=['GET'])
def get_article_by_id(id_article):
    article = query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [id_article])
    return jsonify(article)

@article_bp.route('/article/<int:article_id>')
def get_article(article_id):
    # Récupérez les informations de base de l'article
    article = query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?',(article_id,), one=True)
    
    # Supposons que vous ayez deux requêtes supplémentaires pour récupérer parties et images
    parties = query_db('SELECT * FROM Partie WHERE ID_Article = ? ORDER BY Position', (article_id,))

    images = query_db('SELECT * FROM Image WHERE ID_Partie = ? ORDER BY Position', (article_id,))

    # Transformez les résultats en format JSONs
    article_data = {
        'Titre': article['Titre'],
        'Date_Creation': str(article['Date_Creation']),
        'Mail': article['Email'],
        'Nom': article['Nom'],
        'Nombre_Vues' : article['Nombre_Vues'],
        'Nombre_Likes' : article['Nombre_Likes'],
        'Contenus': []
    }

    for partie in parties:
        article_data['Contenus'].append({
            'type': 'texte', 
            'contenu': partie['Contenu'],
            'position': partie['Position'] 
        })

    for image in images:
        article_data['Contenus'].append({
            'type': 'image', 
            'src': image['URL'],
            'position': image['Position'] 
        })

    # Triez les contenus par position
    article_data['Contenus'].sort(key=lambda x: x['position'])

    return jsonify(article_data)


@article_bp.route('/upload', methods=['POST'])
def file_upload():
    #avoir le chemin du fichier actuel
    path = os.getcwd()
    file = request.files['file']  # 'file' est le nom de la clé correspondant au fichier
    title = request.form.get('title')  # Récupérer d'autres données si nécessaire
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(path+'\\asset\\documents\\', filename))  # Remplacez par le chemin où vous voulez enregistrer le fichier
        return jsonify({"success": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "No file part"}), 400