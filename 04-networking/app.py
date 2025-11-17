import uvicorn
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Connect to Redis (using hostname from Docker network)
try:
    redis_client = redis.Redis(host='redis-cache', port=6379, decode_responses=True)
except Exception as e:
    print(f"Redis connection error: {e}")
    redis_client = None

class Message(BaseModel):
    key: str
    value: str
    ttl: Optional[int] = None

@app.get('/')
def read_root():
    return {
        "message": "Docker Networking Demo - API + Redis",
        "redis_connected": redis_client is not None
    }

@app.get('/health')
def health_check():
    redis_status = "disconnected"
    if redis_client:
        try:
            redis_client.ping()
            redis_status = "connected"
        except:
            redis_status = "error"
    
    return {
        "status": "healthy",
        "redis": redis_status
    }

@app.post('/cache')
def set_cache(message: Message):
    """Store a key-value pair in Redis"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        if message.ttl:
            redis_client.setex(message.key, message.ttl, message.value)
        else:
            redis_client.set(message.key, message.value)
        
        return {
            "message": "Cached successfully",
            "key": message.key,
            "ttl": message.ttl
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/cache/{key}')
def get_cache(key: str):
    """Retrieve a value from Redis"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        value = redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        
        ttl = redis_client.ttl(key)
        return {
            "key": key,
            "value": value,
            "ttl": ttl if ttl > 0 else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/cache/{key}')
def delete_cache(key: str):
    """Delete a key from Redis"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        result = redis_client.delete(key)
        if result == 0:
            raise HTTPException(status_code=404, detail="Key not found")
        
        return {"message": "Key deleted", "key": key}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/cache')
def list_keys():
    """List all keys in Redis"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not connected")
    
    try:
        keys = redis_client.keys('*')
        return {"keys": keys, "count": len(keys)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
