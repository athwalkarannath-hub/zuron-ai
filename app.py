from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app) # क्रॉस-ओरिजिन रिक्वेस्ट सपोर्ट (Vercel Frontend से कनेक्शन के लिए)

# -------------------------------------------------------------
# 1. Safety & Filter Checklist (गलत प्रॉम्प्ट रोकने का सुरक्षा लॉजिक)
# -------------------------------------------------------------
FORBIDDEN_KEYWORDS = ["fake", "nude", "explicit", "violence", "abuse", "deepfake", "harm"]

def check_prompt_safety(prompt):
    prompt_lower = prompt.lower()
    for word in FORBIDDEN_KEYWORDS:
        if word in prompt_lower:
            return False, f"सुरक्षा कारणों से '{word}' जैसे शब्द/प्रॉम्प्ट इस्तेमाल नहीं किए जा सकते।"
    return True, "Safe"

# -------------------------------------------------------------
# 2. Face-Lock & Image-to-Video Engine API
# -------------------------------------------------------------
@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json or {}
    
    user_prompt = data.get('prompt', '')
    image_data = data.get('image', None) # Base64 Image
    master_pin = data.get('pin', '')

    # Master Pin Validation
    if master_pin != "ZURON2026":
        return jsonify({"success": False, "error": "अमान्य ओनरशिप पिन (Unauthorized)"}), 403

    # Safety Check Run
    is_safe, safety_msg = check_prompt_safety(user_prompt)
    if not is_safe:
        return jsonify({"success": False, "error": safety_msg}), 400

    # Face Locking & Video Generation Pipeline
    if image_data:
        # यहाँ आपका इन-हाउस Open-Source Model (CogVideoX/Wan2.1 + LoRA Face Embedding) ट्रिगर होगा
        face_status = "Real Face Locked Successfully"
        video_output_type = "Image-to-Video (Face Consistent)"
    else:
        face_status = "No Image (Text-to-Video Mode)"
        video_output_type = "Text-to-Video"

    # Simulated AI Processing Time
    time.sleep(1.5)

    # Output Data
    response_payload = {
        "success": True,
        "message": "वीडियो सफलतापूर्वक रेंडर हो गई है!",
        "face_lock": face_status,
        "mode": video_output_type,
        "prompt_used": user_prompt,
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-man-standing-in-a-field-looking-at-the-horizon-42999-large.mp4" # आपकी जनरेटेड MP4 लिंक
    }

    return jsonify(response_payload), 200

# -------------------------------------------------------------
# 3. Health Check Root
# -------------------------------------------------------------
@app.route('/')
def home():
    return jsonify({"status": "Zuron AI Independent Engine Active", "version": "1.0.0"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
