import uvicorn
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Counter stored in memory (will reset on code change with bind mount)
visit_count = 0

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.get('/')
def read_root():
    return {
        "message": "Bind Mount Demo - Live Reload",
        "tip": "Change this message in app.py and see it update without rebuilding!"
    }

@app.get('/health')
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get('/counter')
def get_counter():
    """Counter that increments on each call"""
    global visit_count
    visit_count += 1
    return {
        "visits": visit_count,
        "message": "This counter resets when you modify the code!"
    }

@app.post('/items/')
def create_item(item: Item):
    return {
        "message": "Item created",
        "item": item,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
