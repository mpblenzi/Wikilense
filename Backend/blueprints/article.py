from flask import Blueprint, jsonify
from db import *
from flask import request,send_file, make_response
from werkzeug.utils import secure_filename
import os
from colorama import Fore, Style
from docx import Document
import xml.etree.ElementTree as ET
import aspose.words as aw
from bs4 import BeautifulSoup
import datetime

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
@article_bp.route('/<int:article_id>')
def get_article(article_id):
    # Supposons que query_db retourne une liste de dictionnaires pour chaque ligne
    article = query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A INNER JOIN Utilisateur B ON A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [article_id])

    # On s'assure que l'article existe
    if not article:
        return "Article non trouvé", 404

    article_titre = article[0]['Titre']
    print(article_titre)
    
    # Construction du chemin vers le fichier HTML
    path = os.getcwd()
    path_file_html = os.path.join(path, "..", "Frontend", "public", "article", article_titre, f"{article_titre}.html")
    
    # Vérification de l'existence du fichier
    if not os.path.exists(path_file_html):
        return "Fichier HTML non trouvé", 404

    # Renvoyer le fichier HTML
    return send_file(path_file_html)

# Update de l'article dans le back depuis le front (Creation d'un article)
@article_bp.route('/upload', methods=['POST'])
def file_upload():
    #avoir le chemin du fichier actuel
    path = os.getcwd()
    file = request.files['file']  #'file' est le nom de la clé correspondant au fichier
    
    if file:
        #si le fichier et un document word
        if file.filename.endswith('.docx') or file.filename.endswith('.doc') :
            filename = secure_filename(file.filename)
            file.save(os.path.join(path+'\\asset\\documents\\', filename))
            log("Le fichier "+ filename +" a été téléchargé avec succès dans asst/document" )
            return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200
        else :
            log("Le fichier n'est pas un word", "error")
            return jsonify({"error": "File type not allowed"}), 400
        
    else:
        return jsonify({"error": "Document non trouvé"}), 400

@article_bp.route('/create_article2', methods=['POST'])
def create_article2():
    
    path = os.getcwd()
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    path_file_word = os.path.join(path+'\\asset\\documents\\', filename)
    account_id = request.form.get('account_id')
    category_id = request.form.get('category')
    
    title = request.form.get('title')
    
    doc = aw.Document(path_file_word)
    
    # Enable export of fonts
    options = aw.saving.HtmlSaveOptions()
    options.export_font_resources = True    
    
    path_file_html = path+"\\..\\Frontend\\public\\article\\"+title+"\\"+title+".html"
    
    # Save the document as HTML
    doc.save(path+"\\..\\Frontend\\public\\article\\"+title+"\\"+title+".html", options)
    
    rewrite_html(path_file_html)
    
    ajuster_chemins_images(path_file_html, title)
    
    replace_word(path_file_word)
    
    date_creation = datetime.datetime.now()

    post = query_db('INSERT INTO [Wikilense].[dbo].[Article] values (?,?,?,?,0,0,1)', [title, category_id, account_id, date_creation])
    
    post = query_db('INSERT INTO [Wikilense].[dbo].[MotsCles] values (?)', [title.lower()])
    
    log("L'article "+ title +" a été créé avec succès")
    return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200

def rewrite_html(path_file_html):
    # Lire le fichier HTML
    with open(path_file_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Fonction pour vérifier si un élément contient le style CSS spécifié
    def has_style(tag, style):
        return tag.has_attr('style') and style in tag['style']

    # Trouver et supprimer des <p> spécifiques par style CSS
    p_to_remove = soup.find_all(lambda tag: has_style(tag, 'margin-top:0pt; margin-bottom:8pt; line-height:108%; font-size:12pt'))
    for p in p_to_remove:
        p.decompose()

    # Trouver et supprimer des <div> spécifiques par style CSS
    div_to_remove_header = soup.find_all(lambda tag: has_style(tag, '-aw-headerfooter-type:header-primary; clear:both'))
    for div in div_to_remove_header:
        div.decompose()

    div_to_remove_footer = soup.find_all(lambda tag: has_style(tag, '-aw-headerfooter-type:footer-primary; clear:both'))
    for div in div_to_remove_footer:
        div.decompose()

    # Sauvegarder les modifications dans le fichier
    with open(path_file_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def replace_word(path_file_word):
    #replacer le fichier path_file_word par le dossier document traité
    os.replace(path_file_word, os.getcwd()+'\\asset\\documentTraite\\'+os.path.basename(path_file_word))
    
    log("Le fichier "+ os.path.basename(path_file_word) +" a été déplacé dans asset/documentsTraite")
    
    log("Le fichier "+ os.path.basename(path_file_word) +" a été supprimé")

# Exemple de fonction de transformation des chemins d'images en Python
def ajuster_chemins_images(path_fichier_html, title):
    # Lire le fichier HTML
    with open(path_fichier_html, 'r', encoding='utf-8') as file:
        html_content = file.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Supposons que toutes vos images sont dans des balises <img>
    for img in soup.find_all('img'):
        src_original = img['src']
        img['src'] = f"/article/{title}/{src_original}"  # Ajoutez le chemin correct

    # Sauvegarder les modifications dans le fichier
    with open(path_fichier_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))
        
