# 07 - Environment Variables

## Concept
Environment variables allow you to configure containers without modifying code or rebuilding images. They're essential for:
- Configuration management
- Secrets handling
- Different environments (dev/staging/prod)
- Feature flags
- API keys and credentials

## What This Demo Shows
- Setting environment variables in Dockerfile
- Passing env vars at runtime
- Using .env files
- Environment-specific configuration
- Security best practices
- Docker Compose with env vars

## CLI Commands

### 1. Build the image
```bash
docker build -t env-demo .
```

### 2. Run with default environment variables (from Dockerfile)
```bash
docker run -d -p 8000:8000 --name env-app env-demo

# Check configuration
curl http://localhost:8000/config
```

### 3. Override single environment variable
```bash
docker stop env-app && docker rm env-app

docker run -d -p 8000:8000 --name env-app \
  -e DEBUG=true \
  env-demo

curl http://localhost:8000/config
# Notice DEBUG is now true
```

### 4. Set multiple environment variables
```bash
docker stop env-app && docker rm env-app

docker run -d -p 8000:8000 --name env-app \
  -e APP_NAME="Production API" \
  -e APP_VERSION="2.5.0" \
  -e ENVIRONMENT=production \
  -e MAX_CONNECTIONS=500 \
  env-demo

curl http://localhost:8000/
```

### 5. Use environment file
```bash
# Create a .env file
cat > .env << EOF
APP_NAME=Staging App
APP_VERSION=2.0.0
ENVIRONMENT=staging
DEBUG=true
MAX_CONNECTIONS=200
DATABASE_URL=postgresql://user:pass@db:5432/stagingdb
API_KEY=staging-key-123
SECRET_KEY=staging-secret
EOF

# Run with env file
docker stop env-app && docker rm env-app

docker run -d -p 8000:8000 --name env-app \
  --env-file .env \
  env-demo

curl http://localhost:8000/config
```

### 6. View environment variables in container
```bash
# List all env vars
docker exec env-app env

# Check specific variable
docker exec env-app printenv APP_NAME
docker exec env-app printenv DATABASE_URL
```

### 7. Inspect container environment
```bash
docker inspect env-app --format='{{range .Config.Env}}{{println .}}{{end}}'
```

### 8. Run with debug mode
```bash
docker stop env-app && docker rm env-app

docker run -d -p 8000:8000 --name env-app \
  -e DEBUG=true \
  env-demo

# Access debug endpoint
curl http://localhost:8000/env
# Shows all environment variables (only works with DEBUG=true)
```

### 9. Using secrets (basic approach)
```bash
# Store secret in file
echo "my-super-secret-key" > secret.txt

# Mount as secret (read-only)
docker run -d -p 8000:8000 --name env-app \
  -v $(pwd)/secret.txt:/run/secrets/secret_key:ro \
  -e SECRET_KEY_FILE=/run/secrets/secret_key \
  env-demo

# Cleanup
rm secret.txt
```

### 10. Docker Compose with environment variables

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      APP_NAME: Composed App
      APP_VERSION: 3.0.0
      ENVIRONMENT: docker-compose
      DEBUG: "true"
    env_file:
      - .env
```

Run with compose:
```bash
docker-compose up -d
curl http://localhost:8000/config
```

### 11. Environment-specific compose files

**docker-compose.dev.yml**:
```yaml
version: '3.8'
services:
  app:
    environment:
      ENVIRONMENT: development
      DEBUG: "true"
```

**docker-compose.prod.yml**:
```yaml
version: '3.8'
services:
  app:
    environment:
      ENVIRONMENT: production
      DEBUG: "false"
```

Run for dev:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Run for prod:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 12. Cleanup
```bash
docker stop env-app
docker rm env-app
# or
docker-compose down
```

## Security Best Practices

### ❌ DON'T DO THIS
```dockerfile
# Never hardcode secrets in Dockerfile!
ENV SECRET_KEY=my-secret-123
ENV DATABASE_PASSWORD=password123
```

### ✅ DO THIS INSTEAD

1. **Use .env files (not committed to git)**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

2. **Use Docker secrets (Swarm/Kubernetes)**
```bash
echo "secret-value" | docker secret create my_secret -
```

3. **Use secret management services**
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Secret Manager

4. **Pass secrets at runtime**
```bash
docker run -e DATABASE_PASSWORD="$(cat password.txt)" app
```

## Environment Variable Patterns

### 1. Required vs Optional
```python
# Required - crash if missing
DATABASE_URL = os.environ['DATABASE_URL']

# Optional - with default
DEBUG = os.getenv('DEBUG', 'false')
```

### 2. Type Conversion
```python
MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', '100'))
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
```

### 3. Validation
```python
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
assert ENVIRONMENT in ['development', 'staging', 'production']
```

## Common Environment Variables

### Application
```bash
APP_NAME=MyApp
APP_VERSION=1.0.0
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
```

### Database
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
DB_POOL_SIZE=10
DB_TIMEOUT=30
```

### API & Services
```bash
API_KEY=your-api-key
API_URL=https://api.example.com
REDIS_URL=redis://localhost:6379
```

### Feature Flags
```bash
FEATURE_NEW_UI=true
ENABLE_ANALYTICS=false
MAINTENANCE_MODE=false
```

## .gitignore for Environment Files
```
# Environment files
.env
.env.local
.env.*.local
*.env

# Secrets
secrets/
*.key
*.pem
```

## Key Takeaways
- **Never commit secrets** to version control
- Use `.env.example` as a template
- Set defaults in Dockerfile with `ENV`
- Override with `-e` or `--env-file` at runtime
- Different configs for dev/staging/prod
- Validate and sanitize environment variables
- Use secret management in production
- Document required environment variables

## Real-World Example: 12-Factor App
Following [12-Factor App](https://12factor.net/) principles:
- Store config in environment
- Strict separation of config from code
- Environment variables for everything that varies

## Troubleshooting

### Check if env var is set
```bash
docker exec container printenv VAR_NAME
```

### Debug environment issues
```bash
# Run with debug mode
docker run -e DEBUG=true app

# Check logs
docker logs container-name
```

### Override in docker-compose
```bash
# Temporary override
APP_NAME="Test" docker-compose up
```
