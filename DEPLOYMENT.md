# OSINT Platform 2026 - Docker Deployment Guide

## Quick Start

### 1. Prerequisites

- Docker 20.10+ (`docker --version`)
- Docker Compose 1.29+ (`docker-compose --version`)
- At least 8GB available RAM
- 20GB available disk space
- Linux, macOS, or Windows with WSL2

### 2. Clone & Setup

```bash
git clone <repo-url> osint-platform-2026
cd osint-platform-2026

# Run setup script
bash docker-setup.sh
```

### 3. Configure Environment

```bash
# Edit .env and fill in your API keys
nano .env

# Required API keys:
# - JWT_SECRET_KEY: Auto-generated
# - SHODAN_API_KEY: https://www.shodan.io
# - OPENAI_API_KEY: https://platform.openai.com
# - GEOSPY_API_KEY: https://geospy.ai
# - YOUCONTROL_API_KEY: https://youcontrol.com.ua
```

### 4. Start Services

```bash
# Using docker-compose
docker-compose up -d

# Or using Makefile
make up
```

### 5. Verify Setup

```bash
# Check all services are running
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Access services
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Swagger UI: http://localhost:8000/redoc
```

---

## Service Architecture

### 📊 Service Composition

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Nginx Reverse Proxy (Production - optional)   │
│  Port: 80/443                                   │
│                                                 │
└────────┬────────────────────────┬──────────────┘
         │                        │
    ┌────▼────────┐      ┌────────▼─────┐
    │  FastAPI    │      │  Next.js      │
    │  Backend    │      │  Frontend     │
    │  Port: 8000 │      │  Port: 3000   │
    └────┬────────┘      └───────────────┘
         │
    ┌────▼────────────────┐
    │  Celery Workers     │
    │  (4 concurrency)    │
    │  (Chrome/Tor)       │
    └────┬────────────────┘
         │
    ┌────┴────────┬───────────┬──────────┐
    │             │           │          │
┌───▼──┐      ┌───▼──┐   ┌───▼──┐   ┌──▼───┐
│ Postgres  │  │ Redis   │   │ Tor    │   │ Chromium
│ Port: 5432  │  │ Port: 6379 │   │ Port: 9050 │   │
└──────┘  └──────┘   └──────┘   └──────┘
  (DB)    (Cache)    (Proxy)    (Scraping)
```

### Service Details

#### PostgreSQL (Database)
- **Image**: `postgres:15-alpine`
- **Port**: 5432
- **Volume**: `postgres_data:/var/lib/postgresql/data`
- **Health Check**: pg_isready
- **Memory**: Configurable (default: 256MB shared buffers)

#### Redis (Cache & Broker)
- **Image**: `redis:7-alpine`
- **Port**: 6379
- **Volume**: `redis_data:/data`
- **Features**: AOF persistence, LRU eviction, max 512MB
- **Health Check**: PING command

#### Tor (SOCKS Proxy)
- **Image**: `osminogin/tor-simple`
- **Port**: 9050 (SOCKS5)
- **Use**: Anonymized requests from workers

#### FastAPI (Backend)
- **Dockerfile**: `Dockerfile.api` (multi-stage)
- **Port**: 8000
- **Features**: 
  - Uvicorn server
  - Rate limiting
  - JWT authentication
  - Health checks
- **Volume Mounts**:
  - `./app:/app/app` (development)
  - `./reports:/reports` (evidence storage)

#### Celery Workers
- **Dockerfile**: `worker/Dockerfile` (multi-stage)
- **Features**:
  - 4 concurrent tasks
  - Chromium browser for scraping
  - Tor integration
  - Max 1000 tasks per child
- **Volume Mounts**:
  - `/dev/shm:/dev/shm` (Chrome shared memory)
  - `./reports:/reports`

#### Next.js Frontend
- **Dockerfile**: `web/Dockerfile` (multi-stage)
- **Port**: 3000
- **Features**:
  - Server-side rendering
  - Production-optimized build
  - Standalone mode

---

## Deployment Modes

### 1. Development Mode

```bash
# Services with hot reload
docker-compose -f docker-compose.yml up -d

# Logs
docker-compose logs -f api

# Rebuild on code changes
docker-compose build api
docker-compose up -d api
```

### 2. Production Mode (with Nginx)

```bash
# Generate SSL certificates (self-signed example)
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Start with production profile
docker-compose --profile prod up -d

# Verify HTTPS
curl -k https://localhost
```

### 3. Kubernetes Deployment

Convert docker-compose to Kubernetes manifests:

```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-linux-amd64 -o kompose
chmod +x kompose

# Generate manifests
./kompose convert -f docker-compose.yml -o k8s/

# Deploy
kubectl apply -f k8s/
```

---

## Configuration

### Environment Variables

Key variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://osint:password@postgres:5432/osint

# Redis
REDIS_URL=redis://:password@redis:6379/0

# Celery
CELERY_BROKER_URL=redis://:password@redis:6379/0
CELERY_RESULT_BACKEND=redis://:password@redis:6379/1

# Security
JWT_SECRET_KEY=min_32_chars_random_string

# API Keys
SHODAN_API_KEY=xxx
OPENAI_API_KEY=xxx
GEOSPY_API_KEY=xxx
```

### Worker Configuration

Edit `docker-compose.yml` under `worker` service:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G

# Adjust concurrency
CMD ["celery", "-A", "app.tasks.celery_app", "worker", "--loglevel=info", "--concurrency=4"]
```

---

## Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f worker
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 api

# Follow with timestamps
docker-compose logs -f --timestamps api
```

### Execute Commands

```bash
# Database migration
docker-compose exec api python scripts/init_db.py

# Python shell
docker-compose exec api python

# Celery inspection
docker-compose exec worker celery -A app.tasks.celery_app inspect active

# Redis CLI
docker-compose exec redis redis-cli

# PostgreSQL CLI
docker-compose exec postgres psql -U osint -d osint
```

### Database Management

```bash
# Backup database
docker-compose exec postgres pg_dump -U osint osint > backup.sql

# Restore database
docker-compose exec -T postgres psql -U osint osint < backup.sql

# Show running queries
docker-compose exec postgres psql -U osint -c "SELECT * FROM pg_stat_activity;"
```

### Redis Management

```bash
# Monitor commands
docker-compose exec redis redis-cli monitor

# Check memory
docker-compose exec redis redis-cli info memory

# Clear cache
docker-compose exec redis redis-cli FLUSHDB
```

### Celery Management

```bash
# Show active tasks
docker-compose exec worker celery -A app.tasks.celery_app inspect active

# Show stats
docker-compose exec worker celery -A app.tasks.celery_app inspect stats

# Purge queue
docker-compose exec worker celery -A app.tasks.celery_app purge

# Shutdown worker gracefully
docker-compose exec worker celery -A app.tasks.celery_app control shutdown
```

---

## Scaling

### Horizontal Scaling (Multiple Workers)

```bash
# Start 3 worker instances
docker-compose up -d --scale worker=3

# Check running workers
docker-compose ps | grep worker
```

### Vertical Scaling (Resource Limits)

Edit `docker-compose.yml`:

```yaml
worker:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 4G
```

Restart:

```bash
docker-compose up -d worker
```

---

## Monitoring

### Resource Usage

```bash
# Real-time stats
docker stats

# Per-container stats
docker-compose stats

# Container inspection
docker inspect osint-api
docker inspect osint-worker
```

### Health Checks

```bash
# Manual health checks
make health-check

# Or manually:
curl http://localhost:8000/health
docker-compose exec postgres pg_isready -U osint
docker-compose exec redis redis-cli ping
```

### Log Aggregation (Optional)

Add ELK stack or similar:

```yaml
# In docker-compose.yml (example)
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  environment:
    discovery.type: single-node
```

---

## Troubleshooting

### Services Won't Start

```bash
# Check Docker daemon
docker ps

# Check logs
docker-compose logs -f

# Rebuild images
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Issues

```bash
# Test connection
docker-compose exec postgres psql -U osint -d osint -c "SELECT 1"

# Check pg_hba.conf
docker-compose exec postgres cat /var/lib/postgresql/data/pg_hba.conf

# Reset database
docker-compose down -v
docker-compose up -d postgres
make db-init
```

### Worker Not Processing Tasks

```bash
# Check celery status
docker-compose exec worker celery -A app.tasks.celery_app inspect ping

# Check Redis connection
docker-compose exec redis redis-cli

# Check logs
docker-compose logs -f worker

# Restart worker
docker-compose restart worker
```

### Memory Issues

```bash
# Check memory usage
docker stats

# Limit container memory
docker update --memory 2g osint-worker
docker update --memory 1g osint-api

# Clear cache
docker-compose exec redis redis-cli FLUSHDB
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Kill process
kill -9 <PID>

# Or change port in .env
API_PORT=8001
```

---

## Security Best Practices

### 1. Use Strong Passwords

```bash
# Generate strong password
openssl rand -base64 32

# Update in .env
DB_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET_KEY=$(openssl rand -base64 32)
```

### 2. Network Isolation

```bash
# Use custom network (already in docker-compose.yml)
docker network ls
docker network inspect osint-platform-2026_osint-net
```

### 3. SSL/TLS (Production)

```bash
# Generate certificates
certbot certonly --standalone -d yourdomain.com

# Configure nginx.conf with real certs
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;
```

### 4. API Rate Limiting

Already configured in `nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=60r/m;
```

### 5. Container Security Scanning

```bash
# Scan image for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image osint-api:latest
```

---

## Maintenance

### Regular Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec -T postgres pg_dump -U osint osint | \
  gzip > $BACKUP_DIR/osint_$(date +%Y%m%d_%H%M%S).sql.gz

# Backup reports
tar -czf $BACKUP_DIR/reports_$(date +%Y%m%d_%H%M%S).tar.gz reports/

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Log Rotation

Configured in `docker-compose.yml`:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Update Services

```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build

# Verify services
docker-compose ps
```

---

## Performance Tuning

### PostgreSQL

```bash
# Connect to container
docker-compose exec postgres bash

# Optimize
VACUUM ANALYZE;
CREATE INDEX idx_target ON investigations(target_identifier);
```

### Redis

```bash
# Monitor
docker-compose exec redis redis-cli monitor

# Check memory
docker-compose exec redis redis-cli info memory

# Increase maxmemory if needed
docker-compose exec redis redis-cli CONFIG GET maxmemory
```

### Celery

```bash
# Increase concurrency
docker-compose exec worker celery -A app.tasks.celery_app control pool_restart

# Check active tasks
docker-compose exec worker celery -A app.tasks.celery_app inspect active
```

---

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/redoc
- **GitHub**: [Project Repository]
- **Issues**: [GitHub Issues]
- **Docs**: [Wiki/Documentation]

---

**Last Updated**: March 2026
**Version**: 1.0.0
