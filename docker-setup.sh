#!/bin/bash

set -e

echo "🚀 OSINT Platform 2026 - Docker Setup"
echo "======================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please fill in your API keys!"
    echo "📝 Edit .env and set JWT_SECRET_KEY and other required credentials"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p reports
mkdir -p ssl
chmod 755 reports

# Generate a strong JWT secret if not set
if grep -q "JWT_SECRET_KEY=$" .env; then
    echo "🔐 Generating JWT secret..."
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    sed -i "s/JWT_SECRET_KEY=/JWT_SECRET_KEY=$JWT_SECRET/" .env
    echo "✅ JWT secret generated"
fi

# Build images
echo ""
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "✅ OSINT Platform 2026 is starting!"
echo ""
echo "📍 Service URLs:"
echo "   - Frontend: http://localhost:3000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - API Health: http://localhost:8000/health"
echo ""
echo "📝 Next steps:"
echo "   1. Fill in API keys in .env file"
echo "   2. Restart the platform: docker-compose restart"
echo "   3. Check service status: docker-compose ps"
echo "   4. View logs: docker-compose logs -f api"
echo ""
