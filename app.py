import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # फ्रंटएंड से कनेक्ट करने के लिए

# Replicate API Key (इसे आप Render के Environment Variables में भी सेट कर सकते हैं)
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")

@app.route('/')
def home():
    return "Zuron AI Video Backend is Live and Running!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        image_data = data.get('image', '')
        
        print(f"प्राप्त कमांड/प्रॉम्प्ट: {prompt}")
        print(f"इमेज प्राप्त हुई, साइज़: {len(image_data) if image_data else 0}")
        
        # ----------------------------------------------------
        # यहाँ पर आप Replicate या किसी अन्य AI वीडियो API को कॉल कर सकते हैं।
        # जब आप Render में अपनी API Key डालेंगे, तो यह असली वीडियो जनरेट करेगा।
        # ----------------------------------------------------
        
        # फ़िलहाल यह टेस्ट रिस्पॉन्स है जो आपके फ्रंटएंड पर वीडियो शो करेगा
        return jsonify({
            "status": "success",
            "message": f"कमांड मिल गई: '{prompt}'। AI वीडियो तैयार हो रही है!",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"
        }), 200
        
    except Exception as e:
        print(f"एरर आ गया: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
