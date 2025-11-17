# Docker Lab Session - Complete Learning Guide

A comprehensive, hands-on Docker tutorial covering core concepts from basics to advanced topics. Each module includes working code examples and detailed CLI command walkthroughs.

## 📚 Lab Structure

### [01 - Basic FastAPI Application](./01-basic-app)
**Concepts**: Docker fundamentals, images, containers, basic lifecycle
- Building your first Docker image
- Running and managing containers
- Port mapping and networking basics
- Container inspection and logs
- Understanding Dockerfile basics

**Key Commands**: `docker build`, `docker run`, `docker ps`, `docker logs`, `docker exec`

---

### [02 - Docker Volumes](./02-volumes)
**Concepts**: Data persistence, named volumes, volume lifecycle
- Creating and managing volumes
- Persisting data across container restarts
- Sharing data between containers
- Volume inspection and debugging

**Key Commands**: `docker volume create`, `docker volume ls`, `docker volume inspect`, `docker volume rm`

**Demo App**: Visit counter that persists data in Docker volume

---

### [03 - Bind Mounts](./03-bind-mounts)
**Concepts**: Development workflow, live reloading, host-container file sharing
- Mounting host directories into containers
- Live code reloading without rebuilding
- Read-only vs read-write mounts
- Bind mounts vs volumes comparison

**Key Commands**: `docker run -v`, bind mount syntax, development patterns

**Demo App**: FastAPI app with live reload enabled for development

---

### [04 - Docker Networking](./04-networking)
**Concepts**: Container communication, custom networks, service discovery
- Creating custom bridge networks
- Container-to-container communication
- Network isolation and security
- DNS-based service discovery

**Key Commands**: `docker network create`, `docker network connect`, `docker network inspect`

**Demo App**: API server communicating with Redis cache

---

### [05 - Docker Compose](./05-docker-compose)
**Concepts**: Multi-container orchestration, service dependencies, compose files
- Defining multi-container applications in YAML
- Service dependencies and health checks
- Environment-specific configurations
- Managing complete application stacks

**Key Commands**: `docker-compose up`, `docker-compose down`, `docker-compose logs`, `docker-compose ps`

**Demo App**: Full-stack task manager (API + PostgreSQL + Redis)

---

### [06 - Multi-Stage Builds](./06-multi-stage-builds)
**Concepts**: Image optimization, build vs runtime, security hardening
- Reducing image sizes significantly
- Separating build and runtime dependencies
- Running as non-root user
- Build stage targeting

**Key Commands**: `docker build --target`, image size comparison, layer inspection

**Demo App**: Optimized FastAPI app (50-60% smaller images)

---

### [07 - Environment Variables](./07-environment-variables)
**Concepts**: Configuration management, secrets handling, 12-factor app
- Runtime configuration without rebuilding
- Using .env files
- Environment-specific configurations
- Security best practices

**Key Commands**: `docker run -e`, `docker run --env-file`, environment inspection

**Demo App**: Configurable app showcasing environment variable patterns

---

## 🚀 Quick Start

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Basic command line knowledge
- Text editor or IDE

### Verify Docker Installation
```bash
docker --version
docker-compose --version
```

### Running the Labs

Each lab is self-contained. Navigate to any folder and follow its README:

```bash
cd 01-basic-app
docker build -t basic-app .
docker run -d -p 8000:8000 basic-app
curl http://localhost:8000
```

## 📖 Learning Path

### Beginner Path (Start Here)
1. **01-basic-app** - Learn Docker fundamentals
2. **02-volumes** - Understand data persistence
3. **03-bind-mounts** - Development workflows
4. **07-environment-variables** - Configuration basics

### Intermediate Path
5. **04-networking** - Multi-container communication
6. **05-docker-compose** - Orchestrate services
7. **06-multi-stage-builds** - Optimize images

### Recommended Order
Go through labs **01 → 07** sequentially for best learning experience. Each lab builds on concepts from previous ones.

## 🎯 What You'll Learn

### Core Docker Concepts
- ✅ Images vs Containers
- ✅ Dockerfile syntax and best practices
- ✅ Container lifecycle management
- ✅ Port mapping and networking
- ✅ Data persistence strategies
- ✅ Multi-container applications

### Production Skills
- ✅ Image optimization techniques
- ✅ Security hardening (non-root users)
- ✅ Environment-based configuration
- ✅ Service orchestration
- ✅ Health checks and dependencies
- ✅ Development vs production setups

### Practical Workflows
- ✅ Development with live reload
- ✅ Database integration
- ✅ Caching strategies
- ✅ Debugging containers
- ✅ Log management
- ✅ Resource monitoring

## 🛠️ Technologies Used

- **Python 3.9** - Application runtime
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **uv** - Fast Python package manager
- **PostgreSQL** - Relational database
- **Redis** - In-memory cache
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration

## 📝 Docker Command Quick Reference

### Image Management
```bash
docker build -t name .          # Build image
docker images                   # List images
docker rmi image-name          # Remove image
docker history image-name      # View image layers
```

### Container Management
```bash
docker run [options] image     # Create & start container
docker ps                      # List running containers
docker ps -a                   # List all containers
docker stop container          # Stop container
docker start container         # Start container
docker restart container       # Restart container
docker rm container           # Remove container
docker logs container         # View logs
docker exec -it container bash # Execute command
```

### Data Management
```bash
docker volume create name      # Create volume
docker volume ls              # List volumes
docker volume rm name         # Remove volume
docker volume inspect name    # View volume details
```

### Network Management
```bash
docker network create name     # Create network
docker network ls             # List networks
docker network inspect name   # View network details
docker network connect net cont # Connect container to network
```

### Docker Compose
```bash
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f        # Follow logs
docker-compose ps             # List services
docker-compose restart        # Restart services
```

### Cleanup
```bash
docker system prune -a        # Remove all unused resources
docker container prune        # Remove stopped containers
docker image prune           # Remove dangling images
docker volume prune          # Remove unused volumes
```

## Debugging Tips

### Container won't start?
```bash
docker logs container-name
docker run -it image-name /bin/bash
```

### Port already in use?
```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or use a different port
docker run -p 8001:8000 image-name
```

### Application not responding?
```bash
docker ps  # Is it running?
docker logs -f container-name  # Check logs
docker exec container-name curl localhost:8000  # Test from inside
```

### Image too large?
```bash
docker history image-name  # See layer sizes
# Then use multi-stage builds (lab 06)
```


## Additional Resources

### Official Documentation
- [Docker Docs](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

### Best Practices
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [12-Factor App](https://12factor.net/)
- [OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

### Community
- [Docker Hub](https://hub.docker.com/)
- [Docker Community Forums](https://forums.docker.com/)
- [Stack Overflow - Docker Tag](https://stackoverflow.com/questions/tagged/docker)

## Contributing

Found an issue or want to improve a lab? Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Test your changes
4. Submit a pull request

## License

This educational material is provided as-is for learning purposes.

## Acknowledgments

Built with modern tools:
- Docker for containerization
- FastAPI for fast, modern APIs
- uv for blazing-fast Python package management

---

**Happy Learning! 🐳**

Start with `01-basic-app` and work your way through. Each lab takes 15-30 minutes to complete.
