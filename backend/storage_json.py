import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/inquiries.json")

def load_inquiries():
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_inquiry(question: str, category: str, priority: str, answer: str):
    inquiries = load_inquiries()
    
    
    if inquiries:
        new_id = max(item["id"] for item in inquiries) + 1
    else:
        new_id = 1
    
    item = {
        "id": new_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "category": category,
        "priority": priority,
        "answer": answer
    }
    inquiries.append(item)
    DATA_PATH.parent.mkdir(exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(inquiries, f, ensure_ascii=False, indent=2)
    return item

def delete_inquiry(inquiry_id: int):
    """ID နဲ့ဖျက်ပြီး ID များကို ပြန်စီမယ်"""
    inquiries = load_inquiries()
    
    
    new_inquiries = [item for item in inquiries if item["id"] != inquiry_id]
    
    if len(new_inquiries) == len(inquiries):
        return False 
    
    
    for new_id, item in enumerate(new_inquiries, start=1):
        item["id"] = new_id
    
   
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_inquiries, f, ensure_ascii=False, indent=2)
    return True