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
import re

article_bp = Blueprint('article', __name__)

# Récupérer tous les articles d'une catégorie
@article_bp.route('/by_categorie/<int:id_category>', methods=['GET'])
async def get_article_by_category(id_category):
    articles = await query_db('SELECT * FROM Article WHERE [ID_Sous_Sous_Categorie] = ?', [id_category])
    await log("Récupération des articles de la catégorie avec l'id "+ str(id_category), "info")
    return jsonify(articles)

# Récupérer TITRE, DATE_CREATION, NOMBRE_LIKES, NOMBRE_VUES, NOM, EMAIL d'un l'article
@article_bp.route('/by_id/<int:id_article>', methods=['GET'])
async def get_article_by_id(id_article):
    article = await query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A inner join Utilisateur B on A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [id_article])
    
    await log("Récupération de l'article avec l'id "+ str(id_article), "info")
    return jsonify(article)

# Récupérer les parties et images d'un article + trier les contenus par position
@article_bp.route('/<int:article_id>')
async def get_article(article_id):
    # Supposons que await query_db retourne une liste de dictionnaires pour chaque ligne
    article = await query_db('SELECT A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A INNER JOIN Utilisateur B ON A.ID_Utilisateur_Createur = B.ID WHERE A.[ID] = ?', [article_id])

    # On s'assure que l'article existe
    if not article:
        await log("Article non trouvé", "error")
        return "Article non trouvé", 404

    article_titre = article[0]['Titre']
    
    # Construction du chemin vers le fichier HTML
    path = os.getcwd()
    path_file_html = os.path.join(path, "..", "Frontend", "public", "article", article_titre, f"{article_titre}.html")
    
    # Vérification de l'existence du fichier
    if not os.path.exists(path_file_html):
        await log("Fichier HTML non trouvé", "error")
        return "Fichier HTML non trouvé", 404

    # Renvoyer le fichier HTML
    return send_file(path_file_html)

# Update de l'article dans le back depuis le front (Creation d'un article)
@article_bp.route('/upload', methods=['POST'])
async def file_upload():
    #avoir le chemin du fichier actuel
    path = os.getcwd()
    file = request.files['file']  #'file' est le nom de la clé correspondant au fichier
    
    if file:
        #si le fichier et un document word
        if file.filename.endswith('.docx') or file.filename.endswith('.doc') :
            filename = secure_filename(file.filename)
            file.save(os.path.join(path+'\\asset\\documents\\', filename))
            await log("Le fichier "+ filename +" a été téléchargé avec succès dans asst/document", "success" )
            return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200
        else :
            await log("Le fichier n'est pas un word", "error")
            return jsonify({"error": "File type not allowed"}), 400
        
    else:
        return jsonify({"error": "Document non trouvé"}), 400

#create_article2 est une fonction qui permet de créer un article à partir d'un document word
@article_bp.route('/create_article2', methods=['POST'])
async def create_article2():
    
    #avoir le chemin du fichier actuel
    path = os.getcwd()
    
    #récupérer le fichier
    file = request.files['file']
    filename = secure_filename(file.filename)
    path_file_word = os.path.join(path+'\\asset\\documents\\', filename)
    account_id = request.form.get('account_id')
    category_id = request.form.get('category')
    title = request.form.get('title')
    
    # Vérifier si le fichier est un document Word
    doc = aw.Document(path_file_word)
    # Enable export of fonts
    options = aw.saving.HtmlSaveOptions()
    options.export_font_resources = False     
    # Chemin du fichier HTML
    path_file_html = path+"\\..\\Frontend\\public\\article\\"+title+"\\"+title+".html"
    
    # Save the document as HTML
    doc.save(path_file_html, options)
    
    #attendre que le fichier soit converti en html avant de continuer
    
    await log("Le fichier "+ filename +" a été converti en HTML dans le Fontend avec succès", "success")
    
    await rewrite_html(path_file_html)
    
    await ajuster_chemins_images(path_file_html, title)
    
    await replace_word(path_file_word)
    
    await log("L'article "+ title +" a été modifier avec succès", "success")
    
    date_creation = datetime.datetime.now()
    
    #ajouter l'article dans la base de données et les mots clés
    post = await query_db('INSERT INTO [Wikilense].[dbo].[Article] values (?,?,?,?,0,0,1)', [title, category_id, account_id, date_creation])
    post = await query_db('INSERT INTO [Wikilense].[dbo].[MotsCles] values (?)', [title.lower()])
    
    await log("L'article "+ title +" a été créé avec succès", "success")
    
    await beginning_Keywords(title.lower(), )
    
    return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200

async def rewrite_html(path_file_html):
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
    div_to_remove_header = soup.find_all(lambda tag: has_style(tag, 'font-weight:bold; color:#ff0000'))
    for div in div_to_remove_header:
        div.decompose()

    div_to_remove_footer = soup.find_all(lambda tag: has_style(tag, '-aw-headerfooter-type:footer-primary; clear:both'))
    for div in div_to_remove_footer:
        div.decompose()
        
    # Sauvegarder les modifications dans le fichier
    with open(path_file_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))

async def replace_word(path_file_word):
    #replacer le fichier path_file_word par le dossier document traité
    os.replace(path_file_word, os.getcwd()+'\\asset\\documentTraite\\'+os.path.basename(path_file_word))
    
    await log("Le fichier "+ os.path.basename(path_file_word) +" a été déplacé dans asset/documentsTraite", "success")
    
    await log("Le fichier "+ os.path.basename(path_file_word) +" a été supprimé", "success")

# Exemple de fonction de transformation des chemins d'images en Python
async def ajuster_chemins_images(path_fichier_html, title):
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

async def chercher_mot_et_lien(nom_fichier, mot):
    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        contenu_html = fichier.read()
    
    # Charger le document HTML avec BeautifulSoup
    soup = BeautifulSoup(contenu_html, 'html.parser')

    # Rechercher le mot spécifique dans les balises appropriées (par exemple, les balises de texte)
    for texte in soup.find_all(text=True):
        if mot in texte:
            parent = texte.parent
            # Vérifier si le parent est un lien (balise <a>)
            if parent.name == 'a':
                # Vérifier si le lien redirige vers un autre lien
                href = parent.get('href')
                if href.startswith('http'):
                    print(f"Le mot '{mot}' est un lien href redirigeant vers un autre lien: {href}")
                    
async def Recherche_mot_clef(html_content, mot_a_chercher, lien_redirection):
    # Charger le contenu HTML dans BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    print("le mot à chercher est : ", mot_a_chercher)
    print("Contenu HTML chargé avec succès...")
    print(f"Recherche du mot '{mot_a_chercher}' dans le fichier HTML...")

    # Expression régulière pour trouver le mot avec insensibilité à la casse
    regex_mot = re.compile(re.escape(mot_a_chercher), re.IGNORECASE)

    # Trouver tous les éléments de texte contenant le mot à chercher
    balises_texte = soup.find_all(string=regex_mot)

    # Pour chaque balise texte trouvée
    for balise in balises_texte:
        parent = balise.parent
        # Si le parent est un élément a ou script ou title, passer à la prochaine balise
        if parent.name in ["a", "script", "title"]:
            continue
        # Découper la phrase en deux parties : avant et après le mot recherché
        if mot_a_chercher.lower() in balise.lower():
            
            if parent.name == "a":
                continue
            
            # Découper la phrase en deux parties : avant et après le mot recherché
            phrases = re.split(r'(\b' + re.escape(mot_a_chercher) + r'\b)', balise, flags=re.IGNORECASE)

            # Créer une nouvelle balise <span> pour contenir la phrase avant le mot recherché
            span_avant = soup.new_tag("span")
            span_avant.string = ''.join(phrases[:2])  # Concaténer les deux premiers éléments de la liste phrases

            # Créer une nouvelle balise <a> pour le lien de redirection
            nouvelle_balise = soup.new_tag("a", href=lien_redirection, target="_blank")
            nouvelle_balise.string = phrases[1]  # Utiliser le mot recherché comme texte pour la balise <a>

            # Créer une nouvelle balise <span> pour contenir la phrase après le mot recherché
            span_apres = soup.new_tag("span")
            span_apres.string = ''.join(phrases[2:])  # Concaténer les éléments restants de la liste phrases
            
            #retirer le mot recherché de loa balise avant y compris en respectant la casses
            span_avant.string = re.sub(re.escape(mot_a_chercher), '', span_avant.string, flags=re.IGNORECASE)

            print("Phrase avant la modification :", ''.join(phrases))
            print("Phrase après la modification :", span_avant, nouvelle_balise, span_apres)
            
            print("--------------------")
            
            # Insérer les nouvelles balises dans l'arbre DOM
            balise.replace_with(span_avant)
            span_avant.insert_after(nouvelle_balise)
            nouvelle_balise.insert_after(span_apres)

    # Retourner le HTML modifié
    return str(soup)

async def beginning_Keywords(New_Keywords, ):
    # Récupérer les mots clés existants
    existing_keywords = await query_db('SELECT MotCle FROM Keyword')
    existing_keywords = [keyword['MotCle'] for keyword in existing_keywords]

    # Diviser les nouveaux mots clés en une liste
    new_keywords = New_Keywords.split()

    # Ajouter les nouveaux mots clés à la base de données
    for keyword in new_keywords:
        if keyword.lower() not in existing_keywords:
            await query_db('INSERT INTO Keyword (MotCle) VALUES (?)', (keyword.lower(),))

    await log("Les mots clés ont été ajoutés avec succès", "success")