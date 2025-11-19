# 06 - Multi-Stage Builds

## Concept
Multi-stage builds allow you to use multiple `FROM` statements in a Dockerfile. Each stage can use a different base image, and you can copy artifacts from one stage to another. This results in smaller, more secure production images.

## What This Demo Shows
- Multi-stage build optimization
- Image size comparison
- Separating build and runtime dependencies
- Security improvements (non-root user)
- Build cache optimization

## Why Multi-Stage Builds?

### Problems with Single-Stage Builds
- **Large images**: Include build tools not needed at runtime
- **Security risks**: More packages = more vulnerabilities
- **Slower deployments**: Larger images take longer to transfer
- **Build artifacts**: Compilation files, caches remain in image

### Benefits of Multi-Stage Builds
- **Smaller images**: Only runtime dependencies included
- **Better security**: Fewer packages, non-root user
- **Faster deployments**: Smaller images transfer faster
- **Clean separation**: Build vs runtime concerns

## CLI Commands

### 1. Build single-stage image (for comparison)
```bash
docker build -f Dockerfile.single-stage -t app-single-stage .
```

### 2. Build multi-stage image
```bash
docker build -t app-multi-stage .
```

### 3. Compare image sizes
```bash
docker images | grep app-
```

You should see multi-stage is significantly smaller!

### 4. Inspect image layers
```bash
# Single-stage
docker history app-single-stage

# Multi-stage
docker history app-multi-stage
```

### 5. Run multi-stage container
```bash
docker run -d -p 8000:8000 --name multi-stage-app app-multi-stage
```

### 6. Test the application
```bash
curl http://localhost:8000/
curl http://localhost:8000/health

curl -X POST http://localhost:8000/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from multi-stage build!"}'
```

### 7. Verify non-root user
```bash
docker exec multi-stage-app whoami
# Should output: appuser (not root!)

docker exec multi-stage-app id
# Shows user id and groups
```

### 8. Build specific stage (for debugging)
```bash
# Build only the builder stage
docker build --target builder -t app-builder .

# Run builder stage to inspect
docker run --rm -it app-builder /bin/bash
```

### 9. Analyze image with dive (optional tool)
```bash
# Install dive: https://github.com/wagoodman/dive
brew install dive  # macOS
# or download from releases

# Analyze image
dive app-multi-stage
```

### 10. Check for vulnerabilities
```bash
# Using docker scan (if available)
docker scan app-multi-stage

# Or using trivy
# brew install trivy
trivy image app-multi-stage
```

### 11. Build with buildkit for better caching
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with build output
docker build --progress=plain -t app-multi-stage .
```

### 12. Cleanup
```bash
docker stop multi-stage-app
docker rm multi-stage-app
docker rmi app-single-stage app-multi-stage
```

## Dockerfile Multi-Stage Explained

```dockerfile
# Stage 1: Builder
FROM python:3.14.0-slim AS builder
# Install build dependencies
# Build/compile application
# Install all dependencies

# Stage 2: Runtime
FROM python:3.14.0-slim
# Copy only necessary artifacts from builder
COPY --from=builder /path/to/deps /path/to/deps
# Add application code
# Run as non-root user
```

## Advanced Multi-Stage Patterns

### 1. Testing Stage
```dockerfile
FROM python:3.14.0-slim AS builder
# ... build steps

FROM builder AS test
COPY tests/ /app/tests/
RUN pytest

FROM python:3.14.0-slim AS runtime
COPY --from=builder ...
```

Build and test:
```bash
docker build --target test -t app-test .
```

### 2. Development vs Production
```dockerfile
FROM base AS development
# Dev dependencies
CMD ["uvicorn", "--reload"]

FROM base AS production
# Prod dependencies only
CMD ["uvicorn"]
```

Build for dev:
```bash
docker build --target development -t app-dev .
```

### 3. Using Build Arguments
```dockerfile
ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim AS builder
```

Build with custom arg:
```bash
docker build --build-arg PYTHON_VERSION=3.11 -t app .
```

## Real-World Example: Size Comparison

Typical size reductions:
- **Single-stage Python app**: 400-600 MB
- **Multi-stage Python app**: 150-250 MB
- **Savings**: 50-60% smaller!

## Best Practices

1. **Order stages logically**: Build → Test → Runtime
2. **Use specific base images**: `python:3.14.0-slim` not `python:latest`
3. **Copy only what's needed**: Don't COPY everything to runtime
4. **Use .dockerignore**: Exclude unnecessary files
5. **Run as non-root**: Create and switch to non-root user
6. **Leverage build cache**: Put changing layers last
7. **Name stages**: Use `AS stagename` for clarity

## .dockerignore Example
Create `.dockerignore`:
```
__pycache__
*.pyc
*.pyo
*.pyd
.git
.venv
.pytest_cache
*.egg-info
dist
build
```

## Key Takeaways
- Multi-stage builds produce **smaller images**
- **Separate build and runtime** dependencies
- Copy only **necessary artifacts** to final stage
- Improves **security** (fewer packages, non-root user)
- Faster **deployments** (smaller images)
- Use `--target` to build specific stages
- Great for **compiled languages** (Go, Java, etc.)

## Common Use Cases
- Compiled applications (Go, Rust, C++)
- Frontend builds (npm build → serve static files)
- Backend apps (build deps → runtime deps)
- Test stages in CI/CD
- Development vs production images
