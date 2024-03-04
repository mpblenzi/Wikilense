from flask import Blueprint, jsonify
from db import query_db
from flask import Flask, send_from_directory
from flask import request

user_bp = Blueprint('user', __name__)

@user_bp.route('/by_email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    user = query_db('SELECT ID FROM Utilisateur WHERE Email = ?',email, one=True)
    
    #si le retour et null
    if user is None:
        
        return jsonify({'message': 'User not found'}), 404
    else:
        print(email)
        print("-------------------")
        print(user)
        print("-------------------")
        
        return jsonify(user)

# create user 
@user_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    query_db('INSERT INTO Utilisateur (Nom, Email, Token) VALUES (?,?,?)', (data['Nom'], data['Email'], data['Token']))
    return jsonify({'message': 'User created successfully'}), 200
