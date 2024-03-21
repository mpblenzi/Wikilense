from flask import Blueprint, jsonify
from db import query_db, log
from flask import Flask, send_from_directory
from flask import request

user_bp = Blueprint('user', __name__)

@user_bp.route('/by_email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = query_db('SELECT ID, Nom, Email FROM Utilisateur WHERE Email = ?',email, one=True)
    
    #si le retour et null
    if user is None:
        
        log("Récupération échoué de l'utilisateur avec l'email "+ email, "error")
        return jsonify({'message': 'Utilisateur non trouvé', "Status": 404}), 404
    
    else:
        print(email)
        print("-------------------")
        print(user)
        print("-------------------")
        
        return jsonify(user)

# create user 
def create_user(id, nom, email, token):
    print('INSERT INTO Utilisateur (ID, Nom, Email, Token) VALUES (?, ?, ?, ?)', (id, nom, email, token))
    try:
        query_db('INSERT INTO Utilisateur (ID, Nom, Email, Token) VALUES (?, ?, ?, ?)', (id, nom, email, token))   
        log(f"Utilisateur créé avec succès : {email}", "success")
        return True
    except Exception as e:
        log(f"Erreur lors de la création de l'utilisateur {email}: {e}", "error")
        return False

@user_bp.route('/add_user', methods=['POST'])
def route_add_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data or 'token' not in data or 'id' not in data:
        return jsonify({'message': 'Données manquantes'}), 400
    
    success = create_user(data['id'], data['name'], data['email'], data['token'])
    
    if success:
        return jsonify({'message': 'Utilisateur créé avec succès'}), 201
    else:
        return jsonify({'message': 'Erreur lors de la création de l\'utilisateur'}), 500