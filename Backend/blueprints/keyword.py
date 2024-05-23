from flask import Blueprint, jsonify
from utils.db import *
from flask import request,send_file, make_response


keyword_bp = Blueprint('keyword', __name__)

# Route pour la recherche de mots clés sauf 1 mot clé
@keyword_bp.route('/AllKeyOnlyOne', methods=['GET'])
async def AllKeyOnlyOne():
    
    result = await query_db('SELECT * FROM MotsCles WHERE MotCle != ?', (request.args.get('MotCle'),))
    
    return jsonify(result)


    
    
