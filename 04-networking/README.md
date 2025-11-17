# 04 - Docker Networking

## Concept
Docker networking enables containers to communicate with each other and external services. Containers on the same network can reach each other using container names as hostnames.

## What This Demo Shows
- Creating custom Docker networks
- Container-to-container communication
- Service discovery using container names
- Network isolation
- Inspecting network details

## Architecture
```
┌─────────────────┐         ┌─────────────────┐
│   API Container │────────▶│ Redis Container │
│  (Port 8000)    │         │   (Port 6379)   │
└─────────────────┘         └─────────────────┘
         │                           │
         └───────────────────────────┘
              app-network
```

## CLI Commands

### 1. Create a custom network
```bash
docker network create app-network
```

### 2. List networks
```bash
docker network ls
```

### 3. Inspect network details
```bash
docker network inspect app-network
```

### 4. Build the API image
```bash
docker build -t networking-api .
```

### 5. Start Redis container on the network
```bash
docker run -d \
  --name redis-cache \
  --network app-network \
  redis:7-alpine
```

### 6. Start API container on the same network
```bash
docker run -d \
  --name api-server \
  --network app-network \
  -p 8000:8000 \
  networking-api
```

### 7. Test the API - Check health
```bash
curl http://localhost:8000/health
# Should show redis: connected
```

### 8. Store data in Redis via API
```bash
# Set a key-value pair
curl -X POST http://localhost:8000/cache \
  -H "Content-Type: application/json" \
  -d '{"key": "username", "value": "john_doe"}'

# Set with TTL (expires in 60 seconds)
curl -X POST http://localhost:8000/cache \
  -H "Content-Type: application/json" \
  -d '{"key": "session", "value": "abc123", "ttl": 60}'
```

### 9. Retrieve data from Redis
```bash
# Get specific key
curl http://localhost:8000/cache/username

# List all keys
curl http://localhost:8000/cache
```

### 10. Verify container communication
```bash
# Execute command in API container to ping Redis
docker exec api-server ping -c 3 redis-cache

# Check Redis logs
docker logs redis-cache
```

### 11. Test network isolation
```bash
# Create another network
docker network create isolated-network

# Run a container on different network
docker run -d --name isolated-redis --network isolated-network redis:7-alpine

# Try to ping from api-server (should fail)
docker exec api-server ping -c 3 isolated-redis
# This will fail because they're on different networks
```

### 12. Connect container to multiple networks
```bash
# Connect api-server to both networks
docker network connect isolated-network api-server

# Now ping should work
docker exec api-server ping -c 3 isolated-redis
```

### 13. Disconnect from network
```bash
docker network disconnect isolated-network api-server
```

### 14. Inspect what containers are on a network
```bash
docker network inspect app-network --format='{{range .Containers}}{{.Name}} {{end}}'
```

### 15. View container network settings
```bash
docker inspect api-server --format='{{json .NetworkSettings.Networks}}'
```

### 16. Cleanup
```bash
# Stop containers
docker stop api-server redis-cache isolated-redis
docker rm api-server redis-cache isolated-redis

# Remove networks
docker network rm app-network isolated-network
```

## Network Drivers

### Bridge (default)
- Default network driver
- Best for standalone containers
- Containers can communicate via IP

### Host
```bash
# Container uses host network directly (no isolation)
docker run -d --network host networking-api
```

### None
```bash
# Container has no network access
docker run -d --network none networking-api
```

## Key Takeaways
- Containers on the same network can communicate using container names
- Container names act as hostnames (DNS resolution)
- Networks provide isolation between containers
- Custom networks are better than default bridge for multi-container apps
- Use `--network` flag to attach containers to networks
- One container can be on multiple networks
- Network names in code: `redis://redis-cache:6379`

## Common Use Cases
- **Microservices**: API + Database + Cache
- **Development**: App + Database + Message Queue
- **Testing**: Test runner + Test database
