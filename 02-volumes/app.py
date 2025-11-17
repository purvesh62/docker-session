import uvicorn
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()

# Data will be persisted in /data directory (Docker volume)
DATA_FILE = Path("/data/visits.txt")

class Visit(BaseModel):
    timestamp: str
    message: str

@app.get('/')
def read_root():
    return {"message": "Volume Demo - Visit counter"}

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/visit')
def record_visit(visit: Visit):
    """Record a visit to persistent storage"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(DATA_FILE, 'a') as f:
        f.write(f"{visit.timestamp} - {visit.message}\n")
    
    return {"message": "Visit recorded", "data": visit}

@app.get('/visits')
def get_visits():
    """Retrieve all visits from persistent storage"""
    if not DATA_FILE.exists():
        return {"visits": [], "count": 0}
    
    with open(DATA_FILE, 'r') as f:
        visits = f.readlines()
    
    return {
        "visits": [v.strip() for v in visits],
        "count": len(visits)
    }

@app.delete('/visits')
def clear_visits():
    """Clear all visits"""
    if DATA_FILE.exists():
        DATA_FILE.unlink()
    return {"message": "All visits cleared"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
