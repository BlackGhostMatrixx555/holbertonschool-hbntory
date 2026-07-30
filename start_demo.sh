#!/usr/bin/env bash
#
# One-command launcher for demo day.
# Starts every HBntory service via Docker Compose, waits for each one to
# become healthy, and prints a clear status report before you present.
#
# Usage:
#   ./start_demo.sh

set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== HBntory — Demo launcher ==="
echo

# --- 1. Pre-flight checks -------------------------------------------------

if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed or not in PATH.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}✗ Docker daemon is not running. Start Docker Desktop first.${NC}"
    exit 1
fi

if [ ! -f "ai_service/.env" ]; then
    echo -e "${YELLOW}⚠ ai_service/.env not found.${NC}"
    echo "  Creating it from .env.example — you MUST fill in your real GROQ_API_KEY."
    cp ai_service/.env.example ai_service/.env
    echo -e "${RED}  Edit ai_service/.env now, then re-run this script.${NC}"
    exit 1
fi

if grep -q "your_groq_api_key_here" ai_service/.env 2>/dev/null; then
    echo -e "${RED}✗ ai_service/.env still has the placeholder key. Set your real GROQ_API_KEY first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pre-flight checks passed.${NC}"
echo

# --- 2. Build and start everything ----------------------------------------

echo "Starting all services (this can take a minute on first run)..."
export $(grep -v '^#' ai_service/.env | xargs) 2>/dev/null || true
docker compose up --build -d

echo
echo "Waiting for services to become healthy..."
echo

# --- 3. Health checks -------------------------------------------------------

check_url() {
    local name="$1"
    local url="$2"
    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} $name — $url"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 2
    done

    echo -e "  ${RED}✗${NC} $name — $url did not respond after $((max_attempts * 2))s"
    return 1
}

FAILED=0

check_url "Backend (DB + auth API)"     "http://localhost:8000/health"       || FAILED=1
check_url "Product API"                 "http://localhost:8001/products"     || FAILED=1
check_url "AI Query Service"            "http://localhost:8002/health"       || FAILED=1
check_url "Backoffice"                  "http://localhost:8003/login"        || FAILED=1
check_url "Client Web"                  "http://localhost:8080/index.html"   || FAILED=1

echo

if [ $FAILED -eq 1 ]; then
    echo -e "${RED}⚠ One or more services failed to start. Run 'docker compose logs' to investigate.${NC}"
    exit 1
fi

echo -e "${GREEN}=== Everything is up. ===${NC}"
echo
echo "Open these in your browser for the demo:"
echo "  Client Web (chatbot):     http://localhost:8080"
echo "  Backoffice:               http://localhost:8003/login"
echo "  Backend API docs:         http://localhost:8000/docs"
echo
echo "To stop everything after the demo: ./stop_demo.sh"
