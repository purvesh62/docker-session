# 04 - Docker Bind Mounts

## Concept
Bind mounts allow you to mount a file or directory from the host machine into a container. Unlike volumes, bind mounts depend on the host filesystem structure and are perfect for development workflows where you want live code reloading.

## What This Demo Shows
- Using bind mounts for development
- Live code reloading without rebuilding images
- Difference between bind mounts and volumes
- Development vs production container configurations

## CLI Commands

### 1. Build the image
```bash
docker build -t bind-mount-demo .
```

### 2. Run with bind mount (Development Mode)
```bash
# Mount current directory to /app in container
docker run -d -p 8000:8000 --name bind-app \
  -v "$(pwd)":/app \
  bind-mount-demo
```

**For Windows (PowerShell):**
```powershell
docker run -d -p 8000:8000 --name bind-app -v "${PWD}:/app" bind-mount-demo
```

### 3. Test the application
```bash
curl http://localhost:8000/
curl http://localhost:8000/counter
```

### 4. Make live changes - Edit app.py
Open `app.py` and change the message in the root endpoint:
```python
@app.get('/')
def read_root():
    return {
        "message": "I just changed this without rebuilding!",
        "tip": "Bind mounts are awesome for development!"
    }
```

### 5. Test again (no rebuild needed!)
```bash
# Wait a few seconds for uvicorn to reload
sleep 3
curl http://localhost:8000/
```
You should see your changes immediately!

### 6. View container logs
```bash
docker logs bind-app
# You'll see uvicorn detecting file changes and reloading
```

### 7. Run without bind mount (Production Mode)
```bash
# Stop the development container
docker stop bind-app
docker rm bind-app

# Run without bind mount - code is baked into image
docker run -d -p 8000:8000 --name bind-app-prod bind-mount-demo

# Changes to app.py won't affect this container
```

### 8. Compare bind mount vs volume
```bash
# Create a volume
docker volume create test-volume

# Run with volume (for data persistence)
docker run -d -p 8001:8000 --name volume-app \
  -v test-volume:/data \
  bind-mount-demo

# Run with bind mount (for development)
docker run -d -p 8002:8000 --name bind-app-2 \
  -v "$(pwd)":/app \
  bind-mount-demo
```

### 9. Mount specific files (read-only)
```bash
# Mount only app.py as read-only
docker run -d -p 8000:8000 --name bind-app-ro \
  -v "$(pwd)/app.py:/app/app.py:ro" \
  bind-mount-demo
```

### 10. Cleanup
```bash
docker stop bind-app bind-app-prod bind-app-2 bind-app-ro volume-app
docker rm bind-app bind-app-prod bind-app-2 bind-app-ro volume-app
docker volume rm test-volume
```

## Key Takeaways
- **Bind mounts** = Host directory → Container (good for development)
- **Volumes** = Docker-managed storage (good for production data)
- Bind mounts enable live code reloading
- Use `--reload` flag with uvicorn for automatic reloading
- Add `:ro` suffix for read-only mounts
- Bind mounts depend on host filesystem structure

## Development Workflow
1. Build image once
2. Run with bind mount
3. Edit code on host
4. See changes immediately in container
5. No need to rebuild for each change!
