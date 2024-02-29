from flask import Blueprint, jsonify
from db import *
from flask import request
from werkzeug.utils import secure_filename
import os

article_bp = Blueprint('article', __name__)

# Récupérer tous les articles d'une catégorie
@article_bp.route('/by_categorie/<int:id_category>', methods=['GET'])
def get_article_by_category(id_category):
    articles = query_db('SELECT * FROM Article WHERE [ID_Sous_Sous_Categorie] = ?', [id_category])
    log("Récupération des articles de la catégorie avec l'id "+ str(id_category))
    return jsonify(articles)

# Récupérer TITRE, DATE_CREATION, NOMBRE_LIKES, NOMBRE_VUES, NOM, EMAIL d'un l'article
@article_bp.route('/by_id/<int:id_article>', methods=['GET'])
def get_article_by_id(id_article):
    article = query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [id_article])
    
    log("Récupération de l'article avec l'id "+ str(id_article))
    return jsonify(article)

# Récupérer les parties et images d'un article + trier les contenus par position
@article_bp.route('/article/<int:article_id>')
def get_article(article_id):
    # Récupérez les informations de base de l'article
    article = query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?',(article_id,), one=True)
    
    # Deux requêtes supplémentaires pour récupérer parties et images
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

    # Ajoutez les parties et les images à la liste de contenus
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

# Update de l'article dans le back depuis le front (Creation d'un article)
@article_bp.route('/upload', methods=['POST'])
def file_upload():
    #avoir le chemin du fichier actuel
    path = os.getcwd()
    file = request.files['file']  #'file' est le nom de la clé correspondant au fichier
    title = request.form.get('title')  # Récupérer d'autres données si nécessaire
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(path+'\\asset\\documents\\', filename)) # Remplacez par le chemin où vous voulez enregistrer le fichier
        
        log("Le fichier "+ filename +" a été téléchargé avec succès dans asst/document" )
        return jsonify({"success": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "Document non trouvé"}), 400