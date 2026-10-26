import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS इनेबल किया गया है ताकि Vercel वेबसाइट से रिक्वेस्ट आसानी से आ सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    prompt: Optional[str] = None
    image: Optional[str] = None

@app.post("/generate")
async def generate_video(request: VideoRequest):
    try:
        # यहाँ आपका वीडियो जनरेशन का लॉजिक काम करेगा
        print(f"प्राप्त प्रॉम्प्ट: {request.prompt}")
        
        # टेस्टिंग के लिए रिस्पॉन्स (इसे अपने वीडियो जनरेशन कोड से जोड़ सकते हैं)
        return {
            "status": "success",
            "message": "वीडियो सफलतापूर्वक तैयार हो गया है!",
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
