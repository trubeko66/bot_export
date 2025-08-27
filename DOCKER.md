# Docker Deployment Guide

This guide explains how to deploy the Telegram Channel Export Bot using Docker containers.

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or later)
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd bot_export

# Copy environment template
cp .env.template .env
```

### 2. Configure Environment

Edit the `.env` file with your credentials:

```bash
# Required settings
BOT_TOKEN=123456789:your-bot-token-here
API_ID=12345678
API_HASH=your-api-hash-here

# Optional settings (defaults shown)
DEFAULT_FORMAT=json
INCLUDE_MEDIA_BY_DEFAULT=false
MAX_MESSAGES_PER_EXPORT=10000
DEBUG_MODE=false
```

### 3. Deploy with Docker Compose

```bash
# Build and start the bot
docker compose up -d

# View logs
docker compose logs -f telegram-bot

# Stop the bot
docker compose down
```

## 🔧 Advanced Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram bot token from @BotFather | - | ✅ |
| `API_ID` | Telegram API ID from my.telegram.org | - | ✅ |
| `API_HASH` | Telegram API hash from my.telegram.org | - | ✅ |
| `DEFAULT_FORMAT` | Default export format (json/csv/markdown) | `json` | ❌ |
| `INCLUDE_MEDIA_BY_DEFAULT` | Include media files by default | `false` | ❌ |
| `MAX_MESSAGES_PER_EXPORT` | Maximum messages per export | `10000` | ❌ |
| `DEBUG_MODE` | Enable debug logging | `false` | ❌ |

### Docker Compose Services

The `docker-compose.yml` includes:

- **telegram-bot**: Main bot service
- **Resource limits**: Memory and CPU constraints
- **Volume mounts**: Persistent data storage
- **Logging**: Structured logging with rotation

### Volume Mounts

```yaml
volumes:
  - ./exports:/app/exports    # Export files
  - ./data:/app/data         # Bot session data
  - ./logs:/app/logs         # Application logs
```

## 🐳 Manual Docker Commands

If you prefer not to use Docker Compose:

### Build Image

```bash
docker build -t telegram-export-bot .
```

### Run Container

```bash
docker run -d \
  --name telegram-export-bot \
  --restart unless-stopped \
  -e BOT_TOKEN="your-token" \
  -e API_ID="your-api-id" \
  -e API_HASH="your-api-hash" \
  -v $(pwd)/exports:/app/exports \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  telegram-export-bot
```

## 📊 Monitoring and Management

### View Logs

```bash
# Real-time logs
docker compose logs -f telegram-bot

# Last 100 lines
docker compose logs --tail=100 telegram-bot
```

### Check Status

```bash
# Container status
docker compose ps

# Resource usage
docker stats telegram-export-bot
```

### Restart Service

```bash
# Restart bot
docker compose restart telegram-bot

# Rebuild and restart
docker compose up -d --build
```

## 🔒 Security Considerations

### 1. Environment Variables

- Store sensitive data in `.env` file
- Never commit `.env` to version control
- Use Docker secrets in production

### 2. User Permissions

The container runs as non-root user `appuser` for security.

### 3. Network Security

- Bot doesn't expose ports by default
- Only outbound connections to Telegram APIs
- Optional health check endpoint on port 8080

## 📁 Data Persistence

### Export Files

- Location: `./exports/` (host) → `/app/exports/` (container)
- Contains: ZIP archives with exported data
- Automatically cleaned after sending

### Bot Session

- Location: `./data/` (host) → `/app/data/` (container)
- Contains: Telegram session files
- Persists login state between restarts

### Logs

- Location: `./logs/` (host) → `/app/logs/` (container)
- Contains: Application logs
- Rotated automatically

## 🚨 Troubleshooting

### Common Issues

#### 1. Bot Token Invalid

```bash
# Check logs for authentication errors
docker compose logs telegram-bot | grep -i "token"
```

**Solution**: Verify `BOT_TOKEN` in `.env` file

#### 2. Permission Errors

```bash
# Fix volume permissions
sudo chown -R 1000:1000 exports/ data/ logs/
```

#### 3. Memory Issues

```bash
# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G  # Increase from 512M
```

#### 4. Container Won't Start

```bash
# Check build logs
docker compose build --no-cache

# Check container logs
docker compose logs telegram-bot
```

### Debug Mode

Enable debug logging:

```bash
# In .env file
DEBUG_MODE=true

# Restart container
docker compose restart telegram-bot
```

## 🔄 Updates and Maintenance

### Update Bot

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose up -d --build
```

### Backup Data

```bash
# Create backup
tar -czf bot-backup-$(date +%Y%m%d).tar.gz data/ exports/

# Restore backup
tar -xzf bot-backup-20240101.tar.gz
```

### Clean Up

```bash
# Remove old containers and images
docker system prune -a

# Remove specific containers
docker compose down --rmi all --volumes
```

## 📋 Production Deployment

### 1. Use Docker Secrets

```yaml
# docker-compose.prod.yml
services:
  telegram-bot:
    secrets:
      - bot_token
      - api_credentials

secrets:
  bot_token:
    external: true
  api_credentials:
    external: true
```

### 2. Use External Volumes

```yaml
volumes:
  bot_data:
    external: true
    name: telegram_bot_data
```

### 3. Set Up Monitoring

- Use health checks
- Implement log aggregation
- Set up alerts for failures

### 4. Environment Separation

Create separate compose files:
- `docker-compose.yml` (development)
- `docker-compose.prod.yml` (production)
- `docker-compose.override.yml` (local overrides)

## 🆘 Support

If you encounter issues:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review container logs
3. Verify environment configuration
4. Check Docker and system resources

For additional help, refer to:
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Telegram Bot API](https://core.telegram.org/bots/api)