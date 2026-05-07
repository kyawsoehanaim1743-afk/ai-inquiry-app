from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.storage_json import save_inquiry, load_inquiries, delete_inquiry
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"  

def analyze_with_gemini(question: str) -> str:
    model = genai.GenerativeModel(MODEL)
    prompt = f"""
あなたは総務部門の問い合わせ一次回答担当です。
社員からの問い合わせを読み、以下の3点を日本語で返してください。

1. カテゴリ
2. 緊急度（高・中・低）
3. 回答案

問い合わせ: {question}

出力形式は以下のようにしてください:
カテゴリ: [カテゴリ名]
緊急度: [高/中/低]
回答案: [回答内容]
"""
    response = model.generate_content(prompt)
    return response.text

app = FastAPI(title="Inquiry API")

class InquiryRequest(BaseModel):
    question: str
    category: str = ""  
    priority: str = ""
    name: str = ""

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    gemini_result = analyze_with_gemini(request.question)                   # Gemini ကနေ category, priority, answer အကုန်ထုတ်မယ်
    
    lines = gemini_result.strip().split('\n')               # Gemini ရဲ့ result ကို parse လုပ်မယ် (ရိုးရှင်းအောင်)
    category = "その他"
    priority = "中"
    answer = gemini_result
    
    for line in lines:
        if line.startswith("カテゴリ:"):
            category = line.replace("カテゴリ:", "").strip()
        elif line.startswith("緊急度:"):
            priority = line.replace("緊急度:", "").strip()
        elif line.startswith("回答案:"):
            answer = line.replace("回答案:", "").strip()
    
    saved_item = save_inquiry(
        question=request.question,
        category=category,
        priority=priority,
        answer=answer
    )
    return saved_item

@app.get("/inquiries")
def get_all_inquiries():
    return load_inquiries()

@app.delete("/inquiries/{inquiry_id}")
def delete_inquiry_by_id(inquiry_id: int):
    result = delete_inquiry(inquiry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {"message": "Deleted successfully", "id": inquiry_id}