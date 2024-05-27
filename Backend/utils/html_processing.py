import os
from bs4 import BeautifulSoup
import re
import aspose.words as aw
from utils.db import query_db, log
from blueprints.keyword import *

async def rewrite_html(path_file_html):
    with open(path_file_html, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    def has_style(tag, style):
        return tag.has_attr('style') and style in tag['style']
    p_to_remove = soup.find_all(lambda tag: has_style(tag, 'margin-top:0pt; margin-bottom:8pt; line-height:108%; font-size:12pt'))
    for p in p_to_remove:
        p.decompose()
    div_to_remove_header = soup.find_all(lambda tag: has_style(tag, 'font-weight:bold; color:#ff0000'))
    for div in div_to_remove_header:
        div.decompose()
    div_to_remove_footer = soup.find_all(lambda tag: has_style(tag, '-aw-headerfooter-type:footer-primary; clear:both'))
    for div in div_to_remove_footer:
        div.decompose()
    with open(path_file_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))

async def replace_word(path_file_word):
    os.replace(path_file_word, os.path.join(os.getcwd(), 'asset', 'documentTraite', os.path.basename(path_file_word)))

async def ajuster_chemins_images(path_fichier_html, title):
    with open(path_fichier_html, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        src_original = img['src']
        img['src'] = f"/article/{title}/{src_original}"
    with open(path_fichier_html, 'w', encoding='utf-8') as file:
        file.write(str(soup))

async def insert_Keywords(New_Keywords):
    existing_keywords = await query_db('SELECT MotCle FROM MotsCles')
    existing_keywords = [keyword['MotCle'] for keyword in existing_keywords]
    if New_Keywords.lower() not in existing_keywords:
        await query_db('INSERT INTO MotsCles (MotCle) VALUES (?)', (New_Keywords.lower(),))
    await log("Les mots clés ont été ajoutés avec succès", "success")

# Fonction pour insérer la relation dans la table ArticleMotsCles
async def insert_Keywords_by_article(New_Keywords):
    
    Id_New_Keywords = await query_db('SELECT [ID_MotCle] FROM [MotsCles] where [MotCle] = ?', New_Keywords.lower())
    Id_New_Keywords = Id_New_Keywords[0]['ID_MotCle']
    
    id_article = await query_db('SELECT ID FROM Article where [Titre] = ?', New_Keywords.lower())
    id_article = id_article[0]['ID']
        
    await query_db('INSERT INTO ArticleMotsCles ([ID_Article],[ID_MotCle]) VALUES (?,?)', (id_article,Id_New_Keywords))
    
    await log("Les mots clés ont été ajoutés avec succès", "success")

#recherche et remplacement le mot clef dans les articles
async def recherche_mot_clef_By_article(mot_clef):
    
    path_article = os.path.join(os.getcwd(), "..", "Frontend", "public", "article")
    
    redirection = await recherche_lien_fonction_Key_word(mot_clef)    
    
    for root, dirs, files in os.walk(path_article):
        for name in dirs:
            for file in os.listdir(os.path.join(root, name)):
                if file.endswith(".html"):
                    with open(os.path.join(root, name, file), 'r', encoding='utf-8') as html_file:
                        
                        html_content = html_file.read()
                        html_modifier = await recherche_motClef_in_HTML(html_content, mot_clef, redirection)
                        with open(os.path.join(root, name, file), 'w', encoding='utf-8') as file:
                            file.write(html_modifier)
                            file.close()
                            
                        
                    
#fonction pour rechercher le mot clé dans le contenu HTML
async def recherche_motClef_in_HTML(html_content, mot_a_chercher, lien_redirection):
    soup = BeautifulSoup(html_content, 'html.parser')
    regex_mot = re.compile(re.escape(mot_a_chercher), re.IGNORECASE)
    balises_texte = soup.find_all(string=regex_mot)
    for balise in balises_texte:
        parent = balise.parent
        if parent.name in ["a", "script", "title"]:
            continue
        if mot_a_chercher.lower() in balise.lower():
            if parent.name == "a":
                continue
            phrases = re.split(r'(\b' + re.escape(mot_a_chercher) + r'\b)', balise, flags=re.IGNORECASE)
            span_avant = soup.new_tag("span")
            span_avant.string = ''.join(phrases[:2])
            nouvelle_balise = soup.new_tag("a", href=lien_redirection, target="_blank")
            nouvelle_balise.string = phrases[1]
            span_apres = soup.new_tag("span")
            span_apres.string = ''.join(phrases[2:])
            span_avant.string = re.sub(re.escape(mot_a_chercher), '', span_avant.string, flags=re.IGNORECASE)
            balise.replace_with(span_avant)
            span_avant.insert_after(nouvelle_balise)
            nouvelle_balise.insert_after(span_apres)
            await log(f"Le mot clé {mot_a_chercher} a été remplacé par un lien", "success")
    return str(soup)

#recherche de lien pour le mot clé
async def recherche_lien_fonction_Key_word(Titre):
    
    article = await query_db('SELECT A.ID, A.Titre, A.Date_Creation, A.Nombre_Likes, A.Nombre_Vues, B.Nom, B.Email FROM Article A INNER JOIN Utilisateur B ON A.ID_Utilisateur_Createur = B.ID WHERE A.[Titre] = ?', [Titre])
    name = article[0]['ID']
    
    lien_de_redirection =  f"http://localhost:4200/articles/{name}"
    
    return lien_de_redirection

async def find_Key_Word_in_html(titre):
    try:
        print("titre => ", titre)

        All_KeyWord = await SelectAll()
        print("All_KeyWord => ", All_KeyWord)

        # pour chaque mot clé on recherche dans l'article et on remplace par un lien
        for key in All_KeyWord:
            try:
                print("key => ", key)
                
                if 'MotCle' not in key:
                    print(f"Key {key} is missing 'MotCle'")
                    continue
                
                lien_redirection = await recherche_lien_fonction_Key_word(key['MotCle'].lower())
                print("lien_redirection => ", lien_redirection)
                
                if not lien_redirection:
                    print(f"No redirection link found for keyword {key['MotCle']}")
                    continue

                path_article = os.path.join(os.getcwd(), "..", "Frontend", "public", "article", f"{titre}", f"{titre}.html")
                print("path_article => ", path_article)

                try:
                    with open(path_article, 'r', encoding='utf-8') as html_file:
                        html_content = html_file.read()
                    
                    print(f"file => {titre}.html")
                    print("mot_clef => ", key['MotCle'])
                    print("redirection => ", lien_redirection)

                    html_modifier = await recherche_motClef_in_HTML(html_content, key['MotCle'], lien_redirection)
                    
                    with open(path_article, 'w', encoding='utf-8') as file:
                        file.write(html_modifier)
                except FileNotFoundError:
                    print(f"File {path_article} not found.")
                except Exception as file_error:
                    print(f"Error processing file {path_article}: {file_error}")

            except Exception as key_error:
                print(f"Error processing key {key}: {key_error}")
    except Exception as e:
        print("error => ", e)
