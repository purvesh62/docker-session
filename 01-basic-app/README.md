# 01 - Basic FastAPI Application

## Concept
This is the starting point for learning Docker - a simple FastAPI application that demonstrates the fundamentals of containerization: building images, running containers, and basic container management.

## What This Demo Shows
- Basic Dockerfile structure
- Building Docker images
- Running containers
- Port mapping
- Basic container lifecycle management
- Using modern Python package manager (uv)

## Application Overview
A simple REST API with:
- Root endpoint
- Health check endpoint
- CRUD operations for items
- In-memory storage

## CLI Commands

### 1. Build the Docker image
```bash
docker build -t basic-app .
```

Explanation:
- `docker build`: Command to build an image
- `-t basic-app`: Tag the image with name "basic-app"
- `.`: Use current directory as build context

### 2. List Docker images
```bash
docker images
```

You should see `basic-app` in the list.

### 3. Run the container
```bash
docker run -d -p 8000:8000 --name my-app basic-app
```

Explanation:
- `docker run`: Create and start a container
- `-d`: Run in detached mode (background)
- `-p 8000:8000`: Map host port 8000 to container port 8000
- `--name my-app`: Give the container a friendly name
- `basic-app`: Use the "basic-app" image

### 4. List running containers
```bash
docker ps
```

To see all containers (including stopped):
```bash
docker ps -a
```

### 5. Test the application
```bash
# Root endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Get all items
curl http://localhost:8000/items/

# Create an item
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "MacBook Pro", "price": 2500.00, "tax": 250.00}'

# Get specific item
curl http://localhost:8000/items/Laptop
```

### 6. View container logs
```bash
docker logs my-app

# Follow logs (like tail -f)
docker logs -f my-app

# Last 50 lines
docker logs --tail 50 my-app
```

### 7. Execute commands in running container
```bash
# Open shell in container
docker exec -it my-app /bin/bash

# Run a specific command
docker exec my-app python --version
docker exec my-app ls -la /app
```

### 8. Inspect container details
```bash
docker inspect my-app

# Get specific info (IP address)
docker inspect my-app --format='{{.NetworkSettings.IPAddress}}'

# Get environment variables
docker inspect my-app --format='{{range .Config.Env}}{{println .}}{{end}}'
```

### 9. View container resource usage
```bash
docker stats my-app

# All containers
docker stats
```

### 10. Stop the container
```bash
docker stop my-app
```

### 11. Start a stopped container
```bash
docker start my-app
```

### 12. Restart the container
```bash
docker restart my-app
```

### 13. Remove the container
```bash
# Must stop first
docker stop my-app
docker rm my-app

# Force remove (stop and remove)
docker rm -f my-app
```

### 14. Remove the image
```bash
docker rmi basic-app

# Force remove
docker rmi -f basic-app
```

### 15. Build with no cache
```bash
docker build --no-cache -t basic-app .
```

### 16. Run container with interactive mode
```bash
docker run -it -p 8000:8000 basic-app
```

Press `Ctrl+C` to stop.

### 17. Run with custom name and auto-remove
```bash
docker run --rm -d -p 8000:8000 --name temp-app basic-app
```

The `--rm` flag automatically removes the container when it stops.

### 18. View container processes
```bash
docker top my-app
```

## Dockerfile Explained

```dockerfile
# Base image - Python 3.14.0 slim variant (smaller size)
FROM python:3.14.0-slim

# Install uv - modern Python package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory in container
WORKDIR /app

# Copy dependency file
COPY pyproject.toml /app/

# Install dependencies using uv (faster than pip)
RUN uv pip install --system --no-cache -r pyproject.toml

# Copy application code
COPY app.py /app/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Common Docker Commands Cheat Sheet

### Images
```bash
docker images                    # List images
docker build -t name .          # Build image
docker rmi image-name           # Remove image
docker pull image-name          # Download image
docker push image-name          # Upload image
```

### Containers
```bash
docker run image-name           # Create and start container
docker ps                       # List running containers
docker ps -a                    # List all containers
docker stop container-name      # Stop container
docker start container-name     # Start container
docker restart container-name   # Restart container
docker rm container-name        # Remove container
docker logs container-name      # View logs
docker exec -it container bash  # Execute command
```

### Cleanup
```bash
docker system prune             # Remove unused data
docker container prune          # Remove stopped containers
docker image prune              # Remove unused images
docker volume prune             # Remove unused volumes
```

## Best Practices

1. **Use specific base image versions** (not `latest`)
2. **Layer caching**: Put less frequently changing commands first
3. **Multi-stage builds**: For smaller production images (see example 06)
4. **Use .dockerignore**: Exclude unnecessary files
5. **Run as non-root user**: For better security (see example 06)
6. **One process per container**: Follow single responsibility
7. **Use environment variables**: For configuration
8. **Health checks**: Define health check endpoints

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Container exits immediately
```bash
# Check logs
docker logs container-name

# Run in interactive mode to debug
docker run -it basic-app /bin/bash
```

### Can't connect to application
```bash
# Check if port is mapped correctly
docker ps

# Check container is running
docker inspect container-name
```

## Next Steps
- **02-volumes**: Learn about persistent data storage
- **03-bind-mounts**: Development workflow with live reloading
- **04-networking**: Container communication
- **05-docker-compose**: Multi-container applications
- **06-multi-stage-builds**: Optimize image size
- **07-environment-variables**: Configuration management

## Key Takeaways
- Docker packages applications with all dependencies
- Images are blueprints, containers are running instances
- Port mapping: `-p host:container`
- Containers are isolated and ephemeral
- Use `docker logs` for debugging
- Name containers for easier management
