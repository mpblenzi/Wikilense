from flask import Blueprint, jsonify
from db import query_db
from flask import Flask, send_from_directory


image_bp = Blueprint('image', __name__)

@image_bp.route('/images_category/<filename>', methods=['GET'])
def get_images(filename):
    return send_from_directory('asset/category/', filename)
