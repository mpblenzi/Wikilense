from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename
import os
import datetime
import aspose.words as aw
from utils.db import query_db, log  # Importation des fonctions utilitaires pour la base de données et les logs
from utils.html_processing import * # Importation des fonctions de traitement HTML
from utils.validation import validate_file  # Importation de la fonction de validation de fichier

# Création d'un blueprint pour les routes de gestion des articles
article_bp = Blueprint('article', __name__)

# Route pour obtenir les articles par catégorie
@article_bp.route('/by_categorie/<int:id_category>', methods=['GET'])
async def get_article_by_category(id_category):
    articles = await query_db('SELECT * FROM Article WHERE [ID_Sous_Sous_Categorie] = ?', [id_category])
    await log(f"Récupération des articles de la catégorie avec l'id {id_category}", "info")
    return jsonify(articles)

# Route pour obtenir un article par son ID
@article_bp.route('/by_id/<int:id_article>', methods=['GET'])
async def get_article_by_id(id_article):
    article = await query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A INNER JOIN Utilisateur B ON A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [id_article])
    await log(f"Récupération de l'article avec l'id {id_article}", "info")
    return jsonify(article)

# Route pour obtenir le fichier HTML d'un article
@article_bp.route('/<int:article_id>', methods=['GET'])
async def get_article(article_id):
    article = await query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A INNER JOIN Utilisateur B ON A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [article_id])
    if not article:
        await log("Article non trouvé", "error")
        return "Article non trouvé", 404

    article_titre = article[0]['Titre']
    path_file_html = os.path.join(os.getcwd(), "..", "Frontend", "public", "article", article_titre, f"{article_titre}.html")
    if not os.path.exists(path_file_html):
        await log("Fichier HTML non trouvé", "error")
        return "Fichier HTML non trouvé", 404

    return send_file(path_file_html)

# Route pour uploader un fichier
@article_bp.route('/upload', methods=['POST'])
async def file_upload():
    path = os.getcwd()
    file = request.files['file']
    if file and validate_file(file.filename):  # Validation du fichier
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, 'asset', 'documents', filename))  # Sauvegarde du fichier
        await log(f"Le fichier {filename} a été téléchargé avec succès dans asset/documents", "success")
        return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200
    else:
        await log("Le fichier n'est pas un document Word", "error")
        return jsonify({"error": "File type not allowed"}), 400

# Route pour créer un article à partir d'un fichier Word
@article_bp.route('/create_article2', methods=['POST'])
async def create_article2():
    path = os.getcwd()
    file = request.files['file']
    filename = secure_filename(file.filename)
    path_file_word = os.path.join(path, 'asset', 'documents', filename)
    account_id = request.form.get('account_id')
    category_id = request.form.get('category')
    title = request.form.get('title')

    # Conversion du fichier Word en HTML
    doc = aw.Document(path_file_word)
    options = aw.saving.HtmlSaveOptions()
    options.export_font_resources = False
    path_file_html = os.path.join(path, "..", "Frontend", "public", "article", title, f"{title}.html")
    doc.save(path_file_html, options)
    await log(f"Le fichier {filename} a été converti en HTML dans le Frontend avec succès", "success")
    
    # Traitement HTML
    await rewrite_html(path_file_html)
    await ajuster_chemins_images(path_file_html, title)
    await replace_word(path_file_word)
    await log(f"L'article {title} a été modifié avec succès", "success")

    # Insertion de l'article dans la base de données
    date_creation = datetime.datetime.now()
    await query_db('INSERT INTO [Wikilense].[dbo].[Article] values (?,?,?,?,0,0,1)', [title, category_id, account_id, date_creation])
    await log(f"L'article {title} a été créé avec succès", "success")
    
    
    await insert_Keywords(title.lower())
    await insert_Keywords_by_article(title.lower())
    
    # trouve le lien de redirection pour le mot clé EN COURS DE DEVELOPPEMENT
    # await recherche_lien_fonction_Key_word(title.lower())  # Décommenter cette ligne si nécessaire EN COURS DE DEVELOPPEMENT
    
    # await recherche_mot_clef_By_article(title.lower())  # Décommenter cette ligne si nécessaire EN COURS DE DEVELOPPEMENT

    
    
    return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200
