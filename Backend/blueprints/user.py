from flask import Blueprint, jsonify
from db import query_db, log
from flask import Flask, send_from_directory
from flask import request
import asyncio

user_bp = Blueprint('user', __name__)

@user_bp.route('/by_email/<string:email>', methods=['GET'])
async def get_user_by_email(email):
    user = await query_db('SELECT ID, Nom, Email FROM Utilisateur WHERE Email = ?',email, one=True)
    
    #si le retour et null
    if user is None:
        await log("Récupération échoué de l'utilisateur avec l'email "+ email, "error")
        return jsonify({'message': 'Utilisateur non trouvé', "Status": 404}), 404
    else:
        return jsonify(user)

# create user 
async def create_user(id, nom, email, token):
    try:
        await query_db('INSERT INTO Utilisateur (ID, Nom, Email, Token) VALUES (?, ?, ?, ?)', (id, nom, email, token))   
        await log(f"Utilisateur créé avec succès : {email}", "success")
        return True
    except Exception as e:
        await log(f"Erreur lors de la création de l'utilisateur {email}: {e}", "error")
        return False

@user_bp.route('/add_user', methods=['POST'])
async def route_add_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data or 'token' not in data or 'id' not in data:
        return jsonify({'message': 'Données manquantes'}), 400
    
    success = create_user(data['id'], data['name'], data['email'], data['token'])
    
    if success:
        await log("Utilisateur créé avec succès", "success")
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201
    else:
        await log("Erreur lors de la création de l'utilisateur", "error")
        return jsonify({'message': 'Erreur lors de la création de l\'utilisateur'}), 500