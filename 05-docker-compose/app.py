import uvicorn
import redis
import psycopg2
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

app = FastAPI()

# Database connection
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres-db'),
    'database': os.getenv('POSTGRES_DB', 'appdb'),
    'user': os.getenv('POSTGRES_USER', 'appuser'),
    'password': os.getenv('POSTGRES_PASSWORD', 'apppass')
}

# Redis connection
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-cache')
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: str

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Initialize database table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get('/')
def read_root():
    return {
        "message": "Docker Compose Demo - Task Manager",
        "services": ["API", "PostgreSQL", "Redis"]
    }

@app.get('/health')
def health_check():
    postgres_status = "disconnected"
    redis_status = "disconnected"
    
    try:
        conn = get_db_connection()
        conn.close()
        postgres_status = "connected"
    except:
        pass
    
    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        pass
    
    return {
        "status": "healthy",
        "postgres": postgres_status,
        "redis": redis_status
    }

@app.post('/tasks', response_model=TaskResponse)
def create_task(task: Task):
    """Create a new task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s) RETURNING id, created_at',
            (task.title, task.description, task.completed)
        )
        task_id, created_at = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidate cache
        redis_client.delete('tasks:all')
        
        return TaskResponse(
            id=task_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/tasks', response_model=List[TaskResponse])
def get_tasks():
    """Get all tasks (with Redis caching)"""
    # Try cache first
    cached = redis_client.get('tasks:all')
    if cached:
        import json
        return json.loads(cached)
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title, description, completed, created_at FROM tasks ORDER BY created_at DESC')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        tasks = [
            TaskResponse(
                id=row[0],
                title=row[1],
                description=row[2],
                completed=row[3],
                created_at=row[4].isoformat()
            )
            for row in rows
        ]
        
        # Cache for 60 seconds
        import json
        redis_client.setex('tasks:all', 60, json.dumps([task.dict() for task in tasks]))
        
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(task_id: int):
    """Get a specific task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title, description, completed, created_at FROM tasks WHERE id = %s', (task_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskResponse(
            id=row[0],
            title=row[1],
            description=row[2],
            completed=row[3],
            created_at=row[4].isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put('/tasks/{task_id}', response_model=TaskResponse)
def update_task(task_id: int, task: Task):
    """Update a task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE tasks SET title=%s, description=%s, completed=%s WHERE id=%s RETURNING created_at',
            (task.title, task.description, task.completed, task_id)
        )
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidate cache
        redis_client.delete('tasks:all')
        
        return TaskResponse(
            id=task_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=result[0].isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    """Delete a task"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s RETURNING id', (task_id,))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Invalidate cache
        redis_client.delete('tasks:all')
        
        return {"message": "Task deleted", "id": task_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
