from flask import Blueprint, jsonify
from db import query_db, log
from flask import Flask, send_from_directory
import asyncio


image_bp = Blueprint('image', __name__)

@image_bp.route('/images_category/<filename>', methods=['GET'])
async def get_images(filename):
    
    try:
        await log(f"Accès demandé à l'image de catégorie : {filename}", "info")
        return send_from_directory('asset/category/', filename), 200
    except Exception as e:
        await log(f"Erreur lors de l'accès à l'image de catégorie : {filename} : {e}", "error")
        return jsonify({'message': 'Image not found'}), 404

@image_bp.route('/image_article/<filename>', methods=['GET'])
async def get_images_article(filename):
    
    try: 
        await log(f"Accès demandé à l'image d'article : {filename}", "info")
        return send_from_directory('asset/Picture_doc/', filename), 200
    except Exception as e:
        await log(f"Erreur lors de l'accès à l'image d'article : {filename} : {e}", "error")
        return jsonify({'message': 'Image not found'}), 404