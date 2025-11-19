import uvicorn
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Counter stored in memory (will reset on code change with bind mount)
visit_count = 0


class Item(BaseModel):
    name: str
    description: str = None
    price: float


@app.get("/")
def read_root():
    return {
        "message": "Bind Mount Demo - Live Reload",
        "tip": "Change this message in app.py and see it update without rebuilding!",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/counter")
def get_counter():
    """Counter that increments on each call"""
    # Persist counter to a file to demonstrate bind mount effect
    global visit_count

    # Try to read existing counter from file
    try:
        if os.path.exists("counter.json") and os.path.getsize("counter.json") > 0:
            with open("counter.json", "r") as f:
                file_content = json.load(f)
                visit_count = file_content.get("visits", 0)
    except (json.JSONDecodeError, OSError):
        # If file is corrupted or can't be read, start fresh
        visit_count = 0

    # Increment the counter
    visit_count += 1

    # Write the updated content back
    with open("counter.json", "w") as f:
        json.dump({"visits": visit_count}, f)

    return {
        "visits": visit_count,
        "message": "This counter resets when you modify the code!",
    }


@app.post("/items/")
def create_item(item: Item):
    return {
        "message": "Item created",
        "item": item,
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
