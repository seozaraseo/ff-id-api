import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/verify', methods=['GET'])
def verify_player():
    uid = request.args.get('id')
    if not uid:
        return jsonify({"status": "error", "message": "UID missing"}), 400
    
    # গ্যারেনার অফিসিয়াল গেটওয়ে থেকে ডাটা চেক
    url = "https://shop.garena.sg/api/auth/player_id_login"
    try:
        response = requests.post(url, json={"app_id": 100067, "login_id": uid})
        data = response.json()
        if "nickname" in data:
            return jsonify({"status": "success", "player_name": data["nickname"]})
        return jsonify({"status": "error", "message": "Invalid UID"}), 404
    except:
        return jsonify({"status": "error", "message": "Server error"}), 500

if __name__ == '__main__':
    app.run()
