# Chimera Protocol - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Database Setup (2 min)

**Option A: PostgreSQL (Recommended)**
```bash
# Install PostgreSQL if not already installed
# Then create database:
createdb chimera_db
```

**Option B: SQLite (Quick Testing)**
Edit `chimera/settings.py` and change DATABASES to:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 2: Install & Setup (2 min)

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env if using PostgreSQL with custom credentials

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

### Step 3: Start Server (1 min)

```bash
python manage.py runserver
```

Server running at: **http://localhost:8000**

## ✅ Verify Installation

### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "ok": true,
  "data": {
    "status": "healthy",
    "timestamp": "...",
    "database": "connected"
  }
}
```

### Test 2: Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Test 3: Store a Memory
```bash
curl -X POST http://localhost:8000/api/mcp/remember \
  -H "Content-Type: application/json" \
  -d '{
    "text": "My first memory!",
    "conversation_id": "test-123",
    "tags": ["test"]
  }'
```

### Test 4: Search Memories
```bash
curl -X POST http://localhost:8000/api/mcp/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "first memory",
    "top_k": 5
  }'
```

### Test 5: Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-123",
    "message": "Hello!",
    "remember": true
  }'
```

## 📚 Next Steps

1. **Explore API Docs**: http://localhost:8000/swagger/
2. **Admin Panel**: http://localhost:8000/admin/
3. **Read Full README**: See README.md for complete documentation
4. **Check Spec**: See `.kiro/spec.md` for API specification

## 🐛 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running: `pg_isready`
- Check credentials in `.env`
- Or switch to SQLite (see Step 1, Option B)

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### Migration Errors
```bash
# Reset migrations (WARNING: deletes data)
python manage.py migrate --run-syncdb
```

## 🎯 Demo Workflow

1. **Store memories**:
   ```bash
   curl -X POST http://localhost:8000/api/mcp/remember \
     -H "Content-Type: application/json" \
     -d '{"text":"User likes Python","conversation_id":"demo","tags":["preference"]}'
   ```

2. **Search for them**:
   ```bash
   curl -X POST http://localhost:8000/api/mcp/search \
     -H "Content-Type: application/json" \
     -d '{"query":"Python","top_k":3}'
   ```

3. **Inject into conversation**:
   ```bash
   curl -X POST http://localhost:8000/api/mcp/inject \
     -H "Content-Type: application/json" \
     -d '{"conversation_id":"demo","max_memories":5}'
   ```

4. **Trigger spec hook**:
   ```bash
   curl -X POST http://localhost:8000/api/hooks/spec-update \
     -H "Content-Type: application/json" \
     -d '{"type":"demo","path":"/api/demo","method":"GET","description":"Demo endpoint"}'
   
   # Check .kiro/spec.md - it should be updated!
   ```

## 🎥 Video Demo Script

1. Show `.kiro/spec.md` (spec-driven development)
2. Run health check
3. Store 2-3 memories with different content
4. Search and show results
5. Trigger spec hook and show file update
6. Show `.kiro/steering.md` (coding guidelines)

---

**Need help?** Check the full README.md or create an issue on GitHub.
