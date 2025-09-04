# 🚀 Code Snippet Explainer - Docker Setup

This guide will help you set up and run the Code Snippet Explainer application using Docker Compose.

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- OpenAI API key (get one from [OpenAI](https://platform.openai.com/api-keys))

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd code-snippet-explainer
```

### 2. Configure Environment

```bash
# Copy the environment template
cp .env.docker .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Start the Application

**Windows (PowerShell):**

```powershell
.\docker.ps1 up
```

**Linux/Mac:**

```bash
./docker.sh up
```

Or manually:

```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Redis**: localhost:6379

## 📁 Project Structure

```
code-snippet-explainer/
├── backend/                 # FastAPI backend
│   ├── Dockerfile          # Backend container configuration
│   ├── requirements.txt    # Python dependencies
│   └── app/               # Application code
├── frontend/               # React frontend
│   ├── Dockerfile         # Frontend container configuration
│   ├── package.json       # Node dependencies
│   └── src/              # React application
├── docker-compose.yml      # Main compose configuration
├── docker-compose.override.yml  # Development overrides
├── docker.sh              # Linux/Mac management script
├── docker.ps1            # Windows management script
└── .env.docker           # Environment template
```

## 🐳 Docker Commands

### Using the Management Scripts

**Windows:**

```powershell
# Start services
.\docker.ps1 up

# View logs
.\docker.ps1 logs

# Stop services
.\docker.ps1 down

# Rebuild everything
.\docker.ps1 rebuild

# Clean up
.\docker.ps1 clean
```

**Linux/Mac:**

```bash
# Start services
./docker.sh up

# View logs
./docker.sh logs

# Stop services
./docker.sh down

# Rebuild everything
./docker.sh rebuild

# Clean up
./docker.sh clean
```

### Manual Docker Compose Commands

```bash
# Start services
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# View logs
docker-compose -f docker-compose.yml -f docker-compose.override.yml logs -f

# Stop services
docker-compose -f docker-compose.yml -f docker-compose.override.yml down

# Rebuild services
docker-compose -f docker-compose.yml -f docker-compose.override.yml build --no-cache

# Clean up
docker-compose -f docker-compose.yml -f docker-compose.override.yml down -v --remove-orphans
```

## 🔧 Configuration

### Environment Variables

| Variable         | Description          | Default              |
| ---------------- | -------------------- | -------------------- |
| `OPENAI_API_KEY` | Your OpenAI API key  | Required             |
| `DEBUG`          | Enable debug mode    | `true`               |
| `LOG_LEVEL`      | Logging level        | `INFO`               |
| `REDIS_URL`      | Redis connection URL | `redis://redis:6379` |

### Service Configuration

- **Backend**: Python 3.12, FastAPI, runs on port 8000
- **Frontend**: Node.js 18, React + TypeScript, runs on port 5173
- **Redis**: Caching layer, runs on port 6379

## 🚀 Development Workflow

### Making Changes

1. **Backend changes**: The container will auto-reload due to volume mounting
2. **Frontend changes**: Hot reload is enabled via Vite
3. **Environment changes**: Restart services after updating `.env`

### Debugging

```bash
# View all logs
.\docker.ps1 logs

# View backend logs only
.\docker.ps1 logs-backend

# View frontend logs only
.\docker.ps1 logs-frontend

# Enter backend container
.\docker.ps1 shell-backend

# Enter frontend container
.\docker.ps1 shell-frontend
```

## 🧪 Testing

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

### Frontend Testing

```bash
# Access the application
open http://localhost:5173
```

## 🛠️ Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 5173, 8000, and 6379 are available
2. **API key issues**: Verify your OpenAI API key is correct in `.env`
3. **Build failures**: Try rebuilding with `--no-cache`
4. **Permission issues**: Ensure Docker has proper permissions

### Logs and Debugging

```bash
# Check service status
docker-compose ps

# View detailed logs
docker-compose logs [service-name]

# Restart specific service
docker-compose restart [service-name]
```

## 📦 Production Deployment

For production deployment, consider:

1. **Environment variables**: Use Docker secrets or external config
2. **SSL/TLS**: Add reverse proxy (nginx) with SSL certificates
3. **Monitoring**: Add health checks and monitoring
4. **Scaling**: Configure multiple replicas for high availability
5. **Security**: Use Docker secrets for sensitive data

## 🤝 Contributing

1. Make changes to the codebase
2. Test with Docker setup
3. Update documentation as needed
4. Submit pull request

## 📄 License

[Add your license information here]

---

For more information about the application features, see the main README.md file.
