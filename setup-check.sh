#!/bin/bash

echo "🤖 Discord Bot Framework - Setup Verification"
echo "============================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to print info
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

echo "🔍 Checking Prerequisites..."
echo ""

# Check Docker
docker --version > /dev/null 2>&1
print_status $? "Docker installed"

# Check Docker Compose
docker-compose --version > /dev/null 2>&1
print_status $? "Docker Compose installed"

echo ""
echo "📁 Checking Project Structure..."
echo ""

# Check essential files
[ -f "Dockerfile" ]
print_status $? "Dockerfile exists"

[ -f "docker-compose.yml" ]
print_status $? "docker-compose.yml exists"

[ -f "entrypoint.sh" ]
print_status $? "entrypoint.sh exists"

[ -f ".env.example" ]
print_status $? ".env.example template exists"

echo ""
echo "🔧 Checking Configuration..."
echo ""

# Check .env file
if [ -f ".env" ]; then
    print_status 0 ".env file found"
    
    # Check if DISCORD_TOKEN is set
    if grep -q "DISCORD_TOKEN=" .env && ! grep -q "DISCORD_TOKEN=your_bot_token_here" .env && ! grep -q "DISCORD_TOKEN=replaceme" .env; then
        print_status 0 "DISCORD_TOKEN configured"
    else
        print_status 1 "DISCORD_TOKEN needs to be set in .env"
        print_warning "Edit .env and add your Discord bot token"
    fi
    
    # Check LOG_ENVIRONMENT
    if grep -q "LOG_ENVIRONMENT=" .env; then
        log_env=$(grep "LOG_ENVIRONMENT=" .env | cut -d'=' -f2)
        print_status 0 "LOG_ENVIRONMENT set to: $log_env"
    else
        print_info "LOG_ENVIRONMENT not set, will use default (production)"
    fi
else
    print_status 1 ".env file not found"
    print_warning "Run: cp .env.example .env"
    print_warning "Then edit .env with your Discord bot token"
fi

echo ""
echo "🤖 Checking Bot Code Structure..."
echo ""

[ -d "bot" ]
print_status $? "bot/ directory exists"

[ -f "bot/bot.py" ]
print_status $? "bot/bot.py exists"

[ -f "bot/requirements.txt" ]
print_status $? "bot/requirements.txt exists"

[ -d "bot/logging" ]
print_status $? "bot/logging/ directory exists"

[ -f "bot/logging/__init__.py" ]
print_status $? "bot/logging/__init__.py exists"

[ -f "bot/logging/config.py" ]
print_status $? "bot/logging/config.py exists"

[ -f "bot/logging/utils.py" ]
print_status $? "bot/logging/utils.py exists"

echo ""
echo "💾 Checking Data Structure..."
echo ""

[ -d "data" ]
print_status $? "data/ directory exists"

if [ ! -d "data/logs" ]; then
    print_warning "data/logs/ directory will be created automatically"
else
    print_status 0 "data/logs/ directory exists"
fi

echo ""
echo "🔍 Checking Docker Environment..."
echo ""

# Check if Docker is running
docker info > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status 0 "Docker daemon is running"
else
    print_status 1 "Docker daemon is not running"
    print_warning "Start Docker Desktop or Docker service"
fi

# Check for existing containers
if docker ps -a --format "table {{.Names}}" | grep -q "discordbot"; then
    print_info "Found existing 'discordbot' container"
    container_status=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep discordbot | awk '{print $2}')
    if [[ $container_status == "Up" ]]; then
        print_status 0 "Container is running"
    else
        print_warning "Container exists but is not running"
    fi
else
    print_info "No existing 'discordbot' container found"
fi

echo ""
echo "📋 Project Information..."
echo ""

print_info "Project Structure:"
tree -L 3 -I '.git|__pycache__|*.pyc|.env' . 2>/dev/null || find . -name ".git" -prune -o -name "__pycache__" -prune -o -name "*.pyc" -prune -o -type f -print | head -20

echo ""
echo "🚀 Next Steps..."
echo ""

if [ ! -f ".env" ] || grep -q "DISCORD_TOKEN=your_bot_token_here\|DISCORD_TOKEN=replaceme" .env; then
    echo "1. Create and configure .env file:"
    echo "   cp .env.example .env"
    echo "   # Edit .env with your Discord bot token"
    echo ""
fi

echo "2. Start the bot:"
echo "   docker-compose up -d"
echo ""

echo "3. View logs:"
echo "   docker-compose logs -f discordbot"
echo ""

echo "4. Use slash commands in Discord:"
echo "   /ping    - Check bot latency"
echo "   /status  - Show bot statistics"
echo "   /info    - Display bot information"
echo ""

echo "5. For development:"
echo "   # Edit files in bot/ directory"
echo "   # Restart to apply changes:"
echo "   docker-compose restart"
echo ""

echo "📚 Documentation:"
echo "   README.md - Complete setup and usage guide"
echo "   data/LOGGING.md - Logging system documentation"
echo ""

echo "✅ Setup verification complete!"
echo ""
