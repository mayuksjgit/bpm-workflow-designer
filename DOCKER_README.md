# 🐳 BPM Workflow Designer - Docker Edition

A containerized Business Process Management tool optimized for Docker deployment with port 80 exposure.

## 🚀 Quick Start (Docker)

### Option 1: Using Docker Compose (Recommended)
```bash
# Build and start the container
docker-compose up -d

# Access the application
# Open: http://localhost
```

### Option 2: Using Docker Build Scripts (Windows)
```batch
# 1. Build the Docker image
docker-build.bat

# 2. Run the container
docker-run.bat

# 3. Stop when done
docker-stop.bat
```

### Option 3: Manual Docker Commands
```bash
# Build the image
docker build -t bpm-workflow-designer .

# Run the container
docker run -d -p 80:80 --name bpm-tool bpm-workflow-designer

# Access at http://localhost
```

## 🔧 Docker Configuration

### Container Specifications
- **Base Image**: `python:3.11-slim`
- **Exposed Port**: `80`
- **Internal Port**: `80`
- **Data Volume**: `/app/data`
- **User**: Non-root user (`appuser`)
- **Health Check**: Enabled with curl

### Environment Variables
- `GRADIO_SERVER_NAME=0.0.0.0` - Listen on all interfaces
- `GRADIO_SERVER_PORT=80` - Use port 80
- `PYTHONUNBUFFERED=1` - Real-time logging

### Volume Mapping
- **Host**: `bmp_data` (Docker volume)
- **Container**: `/app/data`
- **Purpose**: Persistent storage for workflow files

## 📁 File Structure (Docker Optimized)
```
/app/
├── docker_bmp_tool.py      # Main Docker-optimized application
├── requirements.txt        # Python dependencies
├── data/                   # Persistent data volume
│   └── *.json             # Saved workflow files
└── Dockerfile             # Container build instructions
```

## 🌐 Network Access

### Local Access
- **URL**: http://localhost
- **Port**: 80 (standard HTTP)
- **Protocol**: HTTP

### Production Deployment
- **Reverse Proxy**: Ready for nginx/traefik
- **Load Balancer**: Supports multiple instances
- **SSL**: Add SSL termination at proxy level

## 💾 Data Persistence

### Workflow Storage
- **Location**: `/app/data` inside container
- **Volume**: `bmp_data` Docker volume
- **Backup**: `docker cp bpm-workflow-designer:/app/data ./backup`

### Volume Management
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect bmp_data

# Backup data
docker run --rm -v bmp_data:/data -v $(pwd):/backup alpine tar czf /backup/bmp_backup.tar.gz -C /data .

# Restore data
docker run --rm -v bmp_data:/data -v $(pwd):/backup alpine tar xzf /backup/bmp_backup.tar.gz -C /data
```

## 🔍 Monitoring & Logs

### Container Status
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Check health
docker inspect bpm-workflow-designer | grep Health -A 10
```

### Performance Monitoring
```bash
# Resource usage
docker stats bpm-workflow-designer

# Container info
docker inspect bpm-workflow-designer
```

## 🛠️ Development & Debugging

### Development Mode
```bash
# Run with volume mapping for development
docker run -d -p 80:80 -v $(pwd):/app --name bmp-dev bpm-workflow-designer
```

### Debug Mode
```bash
# Run interactively
docker run -it -p 80:80 bpm-workflow-designer /bin/bash

# Check application logs
docker exec -it bpm-workflow-designer tail -f /var/log/app.log
```

### Hot Reload (Development)
```bash
# Mount source code for development
docker run -d -p 80:80 -v $(pwd):/app -e GRADIO_DEBUG=1 bpm-workflow-designer
```

## 🔒 Security Features

### Container Security
- **Non-root user**: Runs as `appuser` (UID 1000)
- **Minimal base**: Uses slim Python image
- **No shell access**: Production container has no shell
- **Health checks**: Automatic container health monitoring

### Network Security
- **Internal only**: Application binds to container network
- **Port isolation**: Only port 80 exposed
- **No privileged access**: Container runs without privileges

## 🚀 Production Deployment

### Docker Swarm
```yaml
version: '3.8'
services:
  bpm-tool:
    image: bpm-workflow-designer
    ports:
      - "80:80"
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    volumes:
      - bmp_data:/app/data
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bpm-workflow-designer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bpm-tool
  template:
    metadata:
      labels:
        app: bpm-tool
    spec:
      containers:
      - name: bpm-tool
        image: bpm-workflow-designer
        ports:
        - containerPort: 80
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
```

### Reverse Proxy (nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🐛 Troubleshooting

### Common Issues

#### Port 80 Already in Use
```bash
# Check what's using port 80
netstat -tulpn | grep :80

# Use different port
docker run -d -p 8080:80 bpm-workflow-designer
```

#### Container Won't Start
```bash
# Check logs
docker logs bpm-workflow-designer

# Check if image exists
docker images | grep bpm-workflow-designer

# Rebuild image
docker build --no-cache -t bpm-workflow-designer .
```

#### Data Not Persisting
```bash
# Check volume
docker volume inspect bmp_data

# Verify mount
docker exec bpm-workflow-designer ls -la /app/data
```

#### Health Check Failing
```bash
# Check health status
docker inspect bpm-workflow-designer | grep Health -A 10

# Test manually
docker exec bpm-workflow-designer curl -f http://localhost:80/
```

## 📊 Performance Optimization

### Resource Limits
```yaml
services:
  bpm-workflow-designer:
    # ... other config
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### Multi-stage Build (Advanced)
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "docker_bmp_tool.py"]
```

## 🎯 Next Steps

1. **Build Image**: Run `docker-build.bat` or `docker build -t bpm-workflow-designer .`
2. **Start Container**: Run `docker-run.bat` or `docker-compose up -d`
3. **Access Application**: Open http://localhost
4. **Create Workflows**: Start designing your business processes
5. **Save Data**: Workflows persist in Docker volume
6. **Scale Up**: Deploy to production with orchestration

---

**🐳 Your BPM tool is now containerized and ready for production deployment!**