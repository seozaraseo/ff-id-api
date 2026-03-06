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

    # গ্যারেনার অফিসিয়াল এপিআই
    url = "https://shop.garena.sg/api/auth/player_id_login"
    
    # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য Headers (যাতে ব্লক না করে)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    payload = {
        "app_id": 100067,
        "login_id": uid
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        # ডাটা চেক করা হচ্ছে
        if "nickname" in data:
            return jsonify({
                "status": "success",
                "player_name": data["nickname"]
            })
        else:
            # গ্যারেনা থেকে এরর মেসেজ আসলে সেটি দেখানো
            error_msg = data.get("error", "Invalid UID or Region mismatch")
            return jsonify({"status": "error", "message": error_msg}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Server Timeout"}), 500

if __name__ == '__main__':
    app.run()
