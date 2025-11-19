import uvicorn
from uuid import uuid4
from typing import Optional
from fastapi import FastAPI, Request

# Initialize FastAPI app
app = FastAPI()


# In-memory item storage
ITEMS = [
    {
        "_id": str(uuid4()),
        "name": "Sample Item",
        "description": "This is a sample item",
        "price": 10.0,
        "tax": 1.0,
    }
]


@app.get("/")
def read_root():
    return {"message": "Hello World!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/items/")
async def create_item(request: Request):
    item_data = await request.json()

    if item_data.get("_id") is None:
        item_data["_id"] = str(uuid4())
    ITEMS.append(item_data)
    return item_data


@app.get("/items/{item_name}")
def read_item(item_name: str):
    for item in ITEMS:
        if item["name"] == item_name:
            return item
    return {"error": "Item not found"}


@app.get("/items/")
def read_all_items():
    return ITEMS


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
