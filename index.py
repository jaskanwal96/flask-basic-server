from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/login', methods=['PUT'])
def login():
    # Parse the incoming JSON request
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    username = data['username']
    password = data['password']

    # Concatenate username and password, then calculate SHA1 checksum
    token_input = f"{username}{password}"
    token = hashlib.sha1(token_input.encode()).hexdigest()

    # Return the token in the response
    return jsonify({"token": token})

@app.route('/flag', methods=['PUT'])
def flag():
    # This endpoint is only here ato simulate the /flag request
    # Replace this logic with actual flag processing if needed
    data = request.get_json()
    # if not data or 'Flag' not in data:
    #     return jsonify({"error": "Missing Flag"}), 400
    print(data)
    return jsonify({"status": "Flag received successfully!", "flag": data})

if __name__ == '__main__':
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)
