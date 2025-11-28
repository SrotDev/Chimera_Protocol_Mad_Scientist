# Chimera Protocol - Quick Reference Card

## 🚀 Setup (5 Minutes)

```bash
cd Chimera_Protocol_Mad_Scientist
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
createdb chimera_db  # or use SQLite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🔗 URLs

- **API**: http://localhost:8000/api/
- **Docs**: http://localhost:8000/swagger/
- **Admin**: http://localhost:8000/admin/

## 📋 Essential Commands

```bash
# Run server
python manage.py runserver

# Run tests
python manage.py test

# Verify setup
python verify_setup.py

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

## 🎯 20 API Endpoints

### Auth (6)
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh
GET    /api/auth/profile
PUT    /api/auth/profile/update
```

### Conversations (5)
```
GET    /api/conversations
POST   /api/conversations/create
GET    /api/conversations/{id}
PUT    /api/conversations/{id}/update
DELETE /api/conversations/{id}/delete
```

### Memory (7)
```
POST   /api/chat
POST   /api/mcp/remember
POST   /api/mcp/search
POST   /api/mcp/inject
GET    /api/mcp/listMemories
DELETE /api/mcp/memory/{id}/delete
DELETE /api/mcp/conversation/{id}/clear
```

### System (2)
```
GET    /api/health
POST   /api/hooks/spec-update
```

## 🧪 Quick Tests

```bash
# Health
curl http://localhost:8000/api/health

# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Store Memory
curl -X POST http://localhost:8000/api/mcp/remember \
  -H "Content-Type: application/json" \
  -d '{"text":"Test","conversation_id":"c1","tags":["test"]}'

# Search
curl -X POST http://localhost:8000/api/mcp/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Test","top_k":5}'
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main docs |
| `QUICKSTART.md` | 5-min setup |
| `API_REFERENCE.md` | Complete API |
| `FINAL_SUMMARY.md` | Project summary |

## 🎨 Kiro Features

1. **Spec-Driven**: `.kiro/spec.md`
2. **Agent Hooks**: `POST /api/hooks/spec-update`
3. **MCP**: All memory endpoints
4. **Steering**: `.kiro/steering.md`

## 🔧 Tech Stack

- Django 4.2 + DRF 3.14
- PostgreSQL / SQLite
- JWT Authentication
- TF-IDF Vector Search
- Swagger/ReDoc Docs

## 📊 Project Stats

- **Endpoints**: 20
- **Models**: 3
- **Tests**: 8 classes
- **Docs**: 7 files
- **LOC**: ~3,000+

## 🚢 Deploy

```bash
# Railway
railway login && railway init && railway up

# Heroku
heroku create && git push heroku main

# Render
# Connect GitHub repo in dashboard
```

## ⚡ Troubleshooting

**Database Error**: Check PostgreSQL running or use SQLite  
**Port in Use**: `python manage.py runserver 8001`  
**Module Error**: `pip install -r requirements.txt`

## 📞 Help

- Full docs: `README.md`
- API docs: http://localhost:8000/swagger/
- Status: `STATUS.md`

---

**Status**: ✅ Complete | **Endpoints**: 20 | **Ready**: Demo & Deploy
