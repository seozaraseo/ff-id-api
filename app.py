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

    # গ্যারেনার গ্লোবাল রিজিয়ন চেক করার জন্য সবচেয়ে শক্তিশালী এন্ডপয়েন্ট
    url = "https://shop.garena.sg/api/auth/player_id_login"
    
    # এটি গ্যারেনাকে বোঝাবে যে এটি কোনো রোবট নয়, একজন সত্যিকারের ইউজার
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": "https://shop.garena.sg/app/100067/idlogin",
        "Origin": "https://shop.garena.sg"
    }
    
    payload = {
        "app_id": 100067,
        "login_id": uid,
        "app_server_id": 0 # গ্লোবাল সার্ভারের জন্য ০ ব্যবহার করা হয়
    }
    
    try:
        # রিকোয়েস্ট পাঠানোর সময় টাইমআউট সেট করা হয়েছে যাতে সার্ভার হ্যাং না হয়
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        
        if "nickname" in data:
            return jsonify({
                "status": "success",
                "player_name": data["nickname"]
            })
        elif "error" in data:
            return jsonify({"status": "error", "message": f"Garena says: {data['error']}"}), 404
        else:
            return jsonify({"status": "error", "message": "UID Not Found in this Region"}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": "Connection Timeout. Try Again."}), 500

if __name__ == '__main__':
    app.run()
