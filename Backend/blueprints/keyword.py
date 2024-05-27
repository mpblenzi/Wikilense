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

