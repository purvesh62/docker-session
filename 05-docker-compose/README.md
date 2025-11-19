# 05 - Docker Compose

## Concept

Docker Compose is a tool for defining and running multi-container Docker applications. Using a YAML file, you can configure all services, networks, and volumes, then start everything with a single command.

## What This Demo Shows

- Multi-container orchestration
- Service dependencies and health checks
- Environment variables management
- Persistent data with volumes
- Custom networks
- Complete application stack (API + Database + Cache)

## Architecture

```
┌─────────────────┐
│   API Service   │ :8000
│   (FastAPI)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────┐  ┌────────┐
│Redis │  │Postgres│
│:6379 │  │ :5432  │
└──────┘  └────────┘
```

## CLI Commands

### 1. Start all services

```bash
docker-compose up -d
```

The `-d` flag runs containers in detached mode (background).

### 2. View running services

```bash
docker-compose ps
```

### 3. View logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs api

# Follow logs (like tail -f)
docker-compose logs -f api

# Last 50 lines
docker-compose logs --tail=50
```

### 4. Check service health

```bash
curl http://localhost:8000/health
```

### 5. Test the application - CRUD operations

#### Create tasks

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Master Docker fundamentals"}'

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker Compose", "description": "Orchestrate multi-container apps", "completed": false}'
```

#### Get all tasks

```bash
curl http://localhost:8000/tasks
# First call hits database, result is cached in Redis
# Second call within 60s returns cached data
```

#### Get specific task

```bash
curl http://localhost:8000/tasks/1
```

#### Update task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Mastered Docker!", "completed": true}'
```

#### Delete task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

### 6. Execute commands in containers

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U appuser -d appdb

# Query the database
docker-compose exec postgres psql -U appuser -d appdb -c "SELECT * FROM tasks;"

# Access Redis CLI
docker-compose exec redis redis-cli

# Check Redis keys
docker-compose exec redis redis-cli KEYS '*'
```

### 7. Scale services (if applicable)

```bash
# Scale API to 3 instances (requires load balancer config)
docker-compose up -d --scale api=3
```

### 8. Restart services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
```

### 9. Stop services (keeps containers)

```bash
docker-compose stop
```

### 10. Start stopped services

```bash
docker-compose start
```

### 11. Rebuild services

```bash
# Rebuild without cache
docker-compose build --no-cache

# Rebuild and restart
docker-compose up -d --build
```

### 12. View resource usage

```bash
docker-compose top
```

### 13. Remove stopped containers

```bash
docker-compose rm
```

### 14. Stop and remove everything

```bash
# Stop and remove containers, networks
docker-compose down

# Also remove volumes (deletes data!)
docker-compose down -v

# Also remove images
docker-compose down --rmi all
```

## Docker Compose File Explained

### Services

```yaml
services:
  postgres:
    image: postgres:15-alpine # Use existing image
    environment: # Set env variables
      POSTGRES_DB: appdb
    volumes: # Mount volumes
      - postgres-data:/var/lib/postgresql/data
    healthcheck: # Define health check
      test: ["CMD-SHELL", "pg_isready"]
    networks: # Join networks
      - app-network
```

### Depends On

```yaml
api:
  depends_on:
    postgres:
      condition: service_healthy # Wait for health check
```

### Volumes

```yaml
volumes:
  postgres-data: # Named volume (persistent)
```

### Networks

```yaml
networks:
  app-network:
    driver: bridge # Default driver
```

## Development Workflow

### 1. Development mode with live reload

Create `docker-compose.dev.yml`:

```yaml
version: "3.8"

services:
  api:
    build: .
    volumes:
      - ./app.py:/app/app.py # Bind mount for live reload
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Run with:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### 2. Override for production

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  api:
    restart: always
    environment:
      ENVIRONMENT: production
```

Run with:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Useful Commands Cheat Sheet

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Execute command in service
docker-compose exec <service> <command>

# View service status
docker-compose ps

# Scale service
docker-compose up -d --scale <service>=<count>
```

## Key Takeaways

- **Single command** to start entire application stack
- **Declarative configuration** in YAML
- **Service dependencies** with health checks
- **Automatic networking** between services
- **Volume management** for data persistence
- **Environment-specific** overrides (dev/prod)
- **Easy development** workflow
- **Reproducible** environments

## Common Use Cases

- Local development environment
- Integration testing
- Microservices development
- Full-stack applications
- CI/CD pipelines
