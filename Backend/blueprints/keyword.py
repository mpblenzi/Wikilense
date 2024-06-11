from flask import Blueprint, jsonify
from utils.db import *
from flask import request,send_file, make_response


keyword_bp = Blueprint('keyword', __name__)

# Route pour la recherche de mots clés sauf 1 mot clé
@keyword_bp.route('/AllKeyOnlyOne', methods=['GET'])
async def AllKeyOnlyOne():
    
    result = await query_db('SELECT * FROM MotsCles WHERE MotCle != ?', (request.args.get('MotCle'),))
    
    return jsonify(result)

async def insert_Keywords(New_Keywords):
    existing_keywords = await query_db('SELECT MotCle FROM MotsCles')
    existing_keywords = [keyword['MotCle'] for keyword in existing_keywords]
    if New_Keywords.lower() not in existing_keywords:
        await query_db('INSERT INTO MotsCles (MotCle) VALUES (?)', (New_Keywords.lower(),))
        await log("Les mots clés ont été ajoutés avec succès", "success")
    else:
        await log("Les mots clés existent déjà", "error")
    
async def SelectAll():
    result = await query_db('SELECT * FROM MotsCles')
    return result

#fonction pour trouver l'id d'un mot clef par son nom
async def get_id_by_keyword(keyword):
    result = await query_db('SELECT ID_MotCle FROM MotsCles WHERE MotCle = ?', (keyword.lower()))
    return result[0]['ID_MotCle']

@keyword_bp.route('/recherche/<KeyWord>', methods=['GET'])
async def recherche(KeyWord):
    result = await query_db("SELECT B.MotCle, C.Titre, C.Nombre_Vues, C.Nombre_Likes, C.Active, D.Nom, E.Nom as 'Nom_parent', E.Path FROM [Wikilense].[dbo].[ArticleMotsCles] A inner join MotsCles B on A.ID_MotCle = B.ID_MotCle inner join Article C on A.ID_Article = C.ID inner join Categorie D on D.ID = C.ID_Sous_Sous_Categorie inner join Categorie E on E.ID = D.ID_Categorie_Parent WHERE B.MotCle LIKE ?", ('%' + KeyWord + '%',))
    print(result)
    return jsonify(result)