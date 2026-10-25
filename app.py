import os
import time
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

@app.route('/')
def home():
    return "Zuron AI Advanced Video Backend is Live!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'A cinematic moving shot')
        image_data = data.get('image', '')
        
        print(f"प्राप्त प्रॉम्प्ट: {prompt}")
        
        if not REPLICATE_API_TOKEN:
            return jsonify({
                "status": "error",
                "message": "एरर: Render में 'REPLICATE_API_TOKEN' सेट नहीं है!"
            }), 500

        headers = {
            "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        # यहाँ हम ऐसा मॉडल इस्तेमाल कर रहे हैं जो आपके प्रॉम्प्ट और फोटो दोनों को बेहतरीन तरीके से मानेगा
        payload = {
            "version": "3f0457e4619daac51203dee447d59acb2528b74ffbfc251f496f1d6fc31378f8",
            "input": {
                "input_image": image_data,
                "prompt": prompt,
                "motion_bucket_id": 127,  # मोमेंटम कंट्रोल करने के लिए (इसे कम-ज्यादा कर सकते हैं)
                "fps": 8
            }
        }

        response = requests.post("https://api.replicate.com/v1/predictions", json=payload, headers=headers)
        res_data = response.json()
        
        if response.status_code != 201:
            return jsonify({
                "status": "error",
                "message": f"Replicate API Error: {res_data.get('detail', 'Unknown error')}"
            }), 500

        prediction_url = res_data.get("urls", {}).get("get")
        
        video_url = ""
        if prediction_url:
            for _ in range(20):  # थोड़ा और समय ताकि वीडियो स्मूथ बने
                time.sleep(3)
                poll_res = requests.get(prediction_url, headers=headers).json()
                status = poll_res.get("status")
                
                if status == "succeeded":
                    output = poll_res.get("output")
                    if isinstance(output, list) and len(output) > 0:
                        video_url = output[0]
                    elif isinstance(output, str):
                        video_url = output
                    break
                elif status == "failed":
                    break

        if not video_url:
            return jsonify({
                "status": "error",
                "message": "वीडियो जनरेशन में समय लग गया या मॉडल व्यस्त है।"
            }), 500

        return jsonify({
            "status": "success",
            "message": f"प्रॉम्प्ट ('{prompt}') के आधार पर वीडियो तैयार है!",
            "video_url": video_url
        }), 200

    except Exception as e:
        print(f"एरर आ गया: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
