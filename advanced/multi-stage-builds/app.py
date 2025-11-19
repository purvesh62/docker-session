import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    text: str

@app.get('/')
def read_root():
    return {
        "message": "Multi-stage Build Demo",
        "optimization": "Smaller image size with build stages"
    }

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/echo')
def echo_message(msg: Message):
    return {
        "echoed": msg.text,
        "length": len(msg.text)
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
