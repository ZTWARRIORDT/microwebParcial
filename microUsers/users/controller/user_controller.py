from flask import Blueprint, request, jsonify, render_template
from db import db
from users.models.user_model import User
import hashlib

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_controller.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_controller.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

@user_controller.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado exitosamente'})

@user_controller.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado exitosamente'})

@user_controller.route('/users')
def users_page():
    return render_template('users.html')

# Ruta principal redirige a users
@user_controller.route('/')
def index():
    return render_template('users.html')

