from flask import Blueprint, jsonify
from db import *
from flask import request
from werkzeug.utils import secure_filename
import os
from colorama import Fore, Style
from docx import Document
import uuid
import zipfile
import xml.etree.ElementTree as ET
import data_creation

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
        #si le fichier et un document word
        if file.filename.endswith('.docx') or file.filename.endswith('.doc') :
            filename = secure_filename(file.filename)
            file.save(os.path.join(path+'\\asset\\documents\\', filename))
            log("Le fichier "+ filename +" a été téléchargé avec succès dans asst/document" )
            return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200
        else :
            log("Erreur lors du téléchargement du fichier", "error")
            return jsonify({"error": "File type not allowed"}), 400
        
    else:
        return jsonify({"error": "Document non trouvé"}), 400
 
    
@article_bp.route('/create_article', methods=['POST'])
def create_article():
    
    path = os.getcwd()
    file = request.files['file']
    filename = secure_filename(file.filename)
    path_file = os.path.join(path+'\\asset\\documents\\', filename)
    
    
    title = request.form.get('title')  
    
    doc_processor = DocxProcessor(path_file)

    # Exemple d'utilisation des méthodes
    text_content = doc_processor.extract_text()
    images = doc_processor.extract_images('images')
    xml_content = doc_processor.extract_xml('file/docx.xml')
    rels_content = doc_processor.extract_rels('file')
    
    root = doc_processor.extract_xml_by_path('file/docx.xml')

    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    }

    data = data_creation.DatabaseConnection('AZFRCER0300\DWK1', 'Wikilense', 'Wikilense', 'Qgx8NdQk5UKn49cKUVHgBfAd4nqeKZW6EbzkRjxS495ZDNhJw7')

    data.insert_titre(title)

    id_article = data.get_id_article(title)

    print('ID Article: ', id_article)

    position = doc_processor.find_paragraph_by_style(root ,namespaces,data, id_article)

    #supprimer le dossier 'images' en admin
    os.system('rmdir /Q /S images')
    os.system('rmdir /Q /S file')
    
    return jsonify({"success": "File uploaded successfully", "filename": filename, "Status": 200}), 200






class DocxProcessor:
    def __init__(self, doc_path):
        self.doc_path = doc_path
        self.doc = Document(doc_path)

    def extract_text(self):
        extracted_content = [para.text for para in self.doc.paragraphs]
        return extracted_content

    def extract_images(self, output_dir):
        images = []
        output_dir = os.path.join(output_dir, os.path.basename(self.doc_path).split('.')[0])

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for rel in self.doc.part.rels.values():
            if "image" in rel.reltype:
                img_name = os.path.basename(rel.target_ref)
                img_blob = rel.target_part.blob
                img_path = os.path.join(output_dir, img_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_blob)
                images.append(img_path)

        return images

    def extract_xml(self, xml_output_path):
        
        if not os.path.exists('file'):
            os.makedirs('file') 

        xml_content = self.doc._element.xml
        with open(xml_output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        return xml_content

    def extract_rels(self, output_path):
        with zipfile.ZipFile(self.doc_path, 'r') as zip_ref:
            rels_path = 'word/_rels/document.xml.rels'
            zip_ref.extract(rels_path, output_path)

        extracted_path = os.path.join(output_path, rels_path)
        with open(extracted_path, 'r', encoding='utf-8') as f:
            rels_xml_content = f.read()
        return rels_xml_content

    def extract_xml_by_path(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return root

    def find_paragraph_by_style(self, root, namespaces, data, id_article):

        paras = root.findall('.//w:p', namespaces)
        
        position = 0

        for para in paras:
            
            position = self.traitement_text(para, namespaces, position, data, id_article)
            
            position = self.traitement_image(para, namespaces, position, data, id_article)
            
        return position
    
    def traitement_image(self, para, namespaces, position, data, id_article):
        
        #si dans le text il y a des images
        if para.find('.//w:drawing', namespaces) is not None:
            
            #trouver l'id de l'image
            drawing = para.find('.//w:drawing', namespaces)
            blip = drawing.find('.//a:blip', namespaces)
            image_id = blip.attrib['{{{0}}}embed'.format(namespaces['r'])]
            
            #ouvrir le fichier rels pour trouver le nom de l'image
            tree_rels = ET.parse('file/word/_rels/document.xml.rels')
            root_rels = tree_rels.getroot()

            # Chemin vers ton fichier .rels
            rels_path = 'file/word/_rels/document.xml.rels'

            # Namespace utilisé dans le fichier .rels
            rels_namespace = {'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}

            # Charger le contenu XML
            tree = ET.parse(rels_path)
            root = tree.getroot()

            # IDs que tu veux rechercher, par exemple rId8, rId13, etc.
            search_id = image_id   # Ajoute tous les IDs que tu as récupérés

            # Utilisation d'un XPath avec le namespace pour trouver l'élément correspondant
            relationship = root.find(f".//pr:Relationship[@Id='{search_id}']", rels_namespace)
            if relationship is not None:
                target = relationship.attrib.get('Target')
                print(f"ID: {search_id}, Target: {target}")
            else:
                print(f"ID: {search_id} not found.")
                
            print('Position: ', position)
            print('Image ID: ', image_id)
            print('Image name: ', target.split('/')[-1])
            print('-------------------')
            
            #reenregistrer l'image a l'emplacement voulu
            with zipfile.ZipFile(self.doc_path, 'r') as zip_ref:
                img_path = f'word/{target}'
                img_blob = zip_ref.read(img_path)
                img_name = uuid.uuid4().hex+'.png'
                img_path = f'C:/Users/lenzia/OneDrive - Luxottica Group S.p.A/Bureau/Wikilense/wikilense/Backend/asset/Picture_doc/{img_name}'
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_blob)
            
                data.insert_Image(id_article, img_name, position)      
                
            position += 1
        
        return position

    def traitement_text(self, para, namespaces, position, data, id_article):
        
        if para.find('.//w:t', namespaces) is not None:

            texts = para.findall('.//w:t', namespaces)
            
            #si text n'est pas vide ou qu'il y a que des espaces
            if ''.join([text.text for text in texts]).strip() != '':
                
                print('Position: ', position)
                text_list = []
                
                for text in texts:
                    text_list.append(text.text)
                
                text_list = ''.join(text_list)
                print(text_list)
                print('-------------------')

                data.insert_partie(text_list, position, id_article)
                
                position += 1
                
        return position
