import uvicorn
from uuid import uuid4
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    _id: Optional[str] = None
    name: str
    description: str = None
    price: float
    tax: float = None

ITEMS = [{
    "_id": str(uuid4()),
    "name": "Sample Item",
    "description": "This is a sample item",
    "price": 10.0,
    "tax": 1.0
}]

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/health')
def health_check():
    return {"status": "healthy"}

@app.post('/items/')
def create_item(item: Item):
    if item._id is None:
        item._id = str(uuid4())
    ITEMS.append(item)
    return item 

@app.get('/items/{item_name}')
def read_item(item_name: str):
    for item in ITEMS:
        if item.name == item_name:
            return item
    return {"error": "Item not found"}

@app.get('/items/')
def read_all_items():
    return ITEMS

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)