from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # फ्रंटएंड (Vercel) से डेटा लेने के लिए CORS ज़रूरी है

@app.route('/')
def home():
    return "Zuron AI Backend is Live and Running!"

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        image_data = data.get('image', '')
        
        # यहाँ पर प्रिंट करके कंसोल में देख सकते हैं कि डेटा आ गया है
        print(f"प्राप्त हुआ प्रॉम्प्ट: {prompt}")
        print(f"इमेज डेटा साइज: {len(image_data) if image_data else 0} कैरेक्टर्स")
        
        # दुकानदारों के लिए वीडियो/पोस्टर जनरेशन का लॉजिक यहाँ आगे जोड़ा जाएगा
        # फ़िलहाल हम सफलता का रिस्पांस और एक सैंपल वीडियो लिंक भेज रहे हैं
        return jsonify({
            "status": "success",
            "message": "फोटो और प्रॉम्प्ट सफलतापूर्वक मिल गए हैं!",
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
