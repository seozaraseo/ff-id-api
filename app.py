import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # যাতে আপনার অ্যাপ থেকে এটি কল করা যায়

@app.route('/verify', methods=['GET'])
def verify_player():
    uid = request.args.get('id')
    if not uid:
        return jsonify({"status": "error", "message": "UID missing"}), 400

    # সরাসরি গ্যারেনার গেটওয়ে কল করা হচ্ছে
    url = "https://shop.garena.sg/api/auth/player_id_login"
    payload = {
        "app_id": 100067, # Free Fire-এর জন্য নির্দিষ্ট কোড
        "login_id": uid
    }
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        if "nickname" in data:
            return jsonify({
                "status": "success",
                "player_name": data["nickname"]
            })
        else:
            return jsonify({"status": "error", "message": "Invalid UID"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
