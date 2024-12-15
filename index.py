from flask import Flask, request, jsonify
import hashlib
import pandas as pd

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

@app.route('/candle', methods=['POST'])
def candle():
    code = request.args.get('code')
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    hour = request.args.get('hour')

    datetime_pattern = f"{year}-{month.zfill(2)}-{day.zfill(2)} {hour.zfill(2)}"

    
    # Parse the incoming JSON request
    df = pd.read_csv("order_books.csv")
    filtered = df[
        (df['code'] == code) & 
        (df['time'].str.startswith(datetime_pattern))
    ]
    if filtered.empty:
        return jsonify({"error": "No data found for the given parameters"}), 404
    ohlc = {
        "open": int(filtered.iloc[0]['price']),
        "high": int(filtered['price'].max()),
        "low": int(filtered['price'].min()),
        "close": int(filtered.iloc[-1]['price']),
    }
    print(ohlc)
    return ohlc

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
    # Run the server on port 5001
    app.run(host='0.0.0.0', port=5001)
