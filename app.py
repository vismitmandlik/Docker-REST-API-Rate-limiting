from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["5 per minute"])


app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)



@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if username or email already exists
    if mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
        return jsonify({'error': 'Username or email already exists'}), 409

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Save user details
    user_id = mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed_password}).inserted_id

    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if user exists
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'User not found'}), 401

    # Check password
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid password'}), 401

    return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])}), 200

if __name__ == '__main__':
    app.run(debug=True)
