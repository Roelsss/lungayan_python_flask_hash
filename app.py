from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Simple in-memory user store
users_db = {}


@app.route('/gethash', methods=['GET'])
def get_hash():
    # Get the 'text' query parameter (default to 'example' if not provided)
    text = request.args.get('text', 'example')

    # Generate hash for the provided text (you can change 'text' to any string)
    hashed_text = generate_password_hash(text)

    # Return the original text and its hash
    return jsonify({'original': text, 'hashed': hashed_text})


@app.route('/sethash', methods=['POST'])
def set_hash():
    # Get JSON data from the request body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        # Hash the provided password
        hashed_password = generate_password_hash(password)

        # Store the hashed password in the in-memory "users_db"
        users_db[username] = hashed_password

        # Respond with a success message
        return jsonify({'message': 'User registered successfully', 'username': username}), 201
    else:
        # Return an error if username or password is missing
        return jsonify({'error': 'Username and password are required'}), 400


@app.route('/login', methods=['POST'])
def login():
    # Get JSON data from the request body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db:
        # Get the stored hashed password for the given username
        stored_hashed_password = users_db[username]

        # Check if the provided password matches the stored hash
        if check_password_hash(stored_hashed_password, password):
            return jsonify({'message': 'Login successful', 'username': username}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)