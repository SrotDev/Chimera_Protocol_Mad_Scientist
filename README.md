# Chimera Protocol - Backend

> **Kiroween Hackathon Project**: Memory-Augmented Conversational AI with MCP

A Django REST Framework backend implementing persistent memory storage and semantic search for conversational AI. Built with spec-driven development, agent hooks, and full MCP (Model Context Protocol) integration.

## 🎯 Project Overview

Chimera Protocol provides a complete backend API for conversational AI with:
- **Django REST Framework** for robust API endpoints
- **PostgreSQL** for reliable data persistence
- **TF-IDF Vector Search** for semantic memory retrieval
- **JWT Authentication** for secure access
- **MCP Protocol** for standardized memory operations
- **Agent Hooks** for dynamic spec updates

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (or SQLite for testing)
- pip

### Installation

```bash
# 1. Navigate to project
cd Chimera_Protocol_Mad_Scientist

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Create database (PostgreSQL)
createdb chimera_db

# 6. Run migrations
python manage.py makemigrations
python manage.py migrate

# 7. Create admin user
python manage.py createsuperuser

# 8. Start server
python manage.py runserver
```

**Windows Users**: Run `setup.bat` for automated setup.

Server will be available at: `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Interactive Docs
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### API Endpoints (20 Total)

#### Health & Status
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/health` | GET | No | Health check |

#### Authentication (6 endpoints)
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/register` | POST | No | Register new user |
| `/api/auth/login` | POST | No | Login user |
| `/api/auth/logout` | POST | Yes | Logout user |
| `/api/auth/refresh` | POST | No | Refresh access token |
| `/api/auth/profile` | GET | Yes | Get user profile |
| `/api/auth/profile/update` | PUT | Yes | Update profile |

#### Conversations (5 endpoints)
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/conversations` | GET | Yes | List all conversations |
| `/api/conversations/create` | POST | Yes | Create conversation |
| `/api/conversations/{id}` | GET | Yes | Get conversation details |
| `/api/conversations/{id}/update` | PUT | Yes | Update conversation |
| `/api/conversations/{id}/delete` | DELETE | Yes | Delete conversation |

#### Chat & Memory (7 endpoints)
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/chat` | POST | No | Chat with optional memory |
| `/api/mcp/remember` | POST | No | Store memory |
| `/api/mcp/search` | POST | No | Search memories |
| `/api/mcp/inject` | POST | No | Inject context |
| `/api/mcp/listMemories` | GET | No | List memories |
| `/api/mcp/memory/{id}/delete` | DELETE | No | Delete specific memory |
| `/api/mcp/conversation/{id}/clear` | DELETE | No | Clear all conversation memories |

#### Agent Hooks (1 endpoint)
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/hooks/spec-update` | POST | No | Auto-update spec.md |

### Example Requests

#### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "password": "securepass123"
  }'
```

#### Store Memory
```bash
curl -X POST http://localhost:8000/api/mcp/remember \
  -H "Content-Type: application/json" \
  -d '{
    "text": "User prefers Python programming",
    "conversation_id": "conv-123",
    "tags": ["preference", "programming"]
  }'
```

#### Search Memories
```bash
curl -X POST http://localhost:8000/api/mcp/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "programming languages",
    "top_k": 5
  }'
```

#### Chat with Memory
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv-123",
    "message": "What do I like?",
    "remember": true
  }'
```

## 🏗️ Project Structure

```
Chimera_Protocol_Mad_Scientist/
├── .kiro/
│   ├── spec.md              # API specification
│   └── steering.md          # Coding guidelines
├── chimera/                 # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                     # Main API app
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API endpoints (20 views)
│   ├── urls.py             # URL routing
│   ├── memory_service.py   # Vector search
│   ├── admin.py            # Admin config
│   └── tests.py            # Unit tests
├── requirements.txt
├── .env.example
├── manage.py
├── setup.bat               # Windows setup
└── README.md
```

## 🎨 Kiro Features

### 1. Spec-Driven Development ✅
- **File**: `.kiro/spec.md`
- Complete API specification written before implementation
- All 20 endpoints documented with request/response schemas

### 2. Agent Hooks ✅
- **Endpoint**: `/api/hooks/spec-update`
- Auto-appends new endpoint definitions to spec.md
- Demonstrates agent-driven spec modifications

### 3. MCP Protocol ✅
- **Files**: `api/views.py`, `api/memory_service.py`
- Full implementation: remember, search, inject, list, delete
- TF-IDF vector search with cosine similarity

### 4. Steering Documents ✅
- **File**: `.kiro/steering.md`
- Comprehensive coding guidelines
- API response format standards
- Memory management rules

## 🗄️ Database Models

### Memory
Stores conversation memories with vector embeddings
- `text`: Memory content
- `tags`: Categorization tags
- `conversation_id`: Associated conversation
- `embedding`: Vector for similarity search
- `metadata`: Additional data

### Conversation
Tracks conversation sessions
- `id`: UUID primary key
- `user`: Foreign key to User
- `title`: Conversation title
- `created_at`, `updated_at`: Timestamps

### ChatMessage
Individual chat messages
- `conversation`: Foreign key
- `role`: user/assistant/system
- `content`: Message text
- `metadata`: Additional data

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific test
python manage.py test api.tests.AuthTestCase

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage
- Authentication tests
- Conversation management tests
- Memory operations tests
- MCP endpoint tests
- Spec hook tests

## 🔧 Configuration

### Environment Variables (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=chimera_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Database Options

**PostgreSQL** (Recommended):
```bash
createdb chimera_db
```

**SQLite** (Quick Testing):
Edit `chimera/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 🚢 Deployment

### Quick Deploy - Railway
```bash
# Install CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add postgresql
railway up
railway run python manage.py migrate
```

### Other Platforms
- **Render**: Connect GitHub, add PostgreSQL, deploy
- **Heroku**: `heroku create`, add postgres addon, push
- **DigitalOcean**: App Platform with managed database

See `DEPLOYMENT_CHECKLIST.md` for detailed guides.

## 🎬 Demo Workflow

1. **Show Spec**: Open `.kiro/spec.md`
2. **Health Check**: `curl http://localhost:8000/api/health`
3. **Register User**: POST to `/api/auth/register`
4. **Store Memories**: POST to `/api/mcp/remember` (3 memories)
5. **Search**: POST to `/api/mcp/search`
6. **Trigger Hook**: POST to `/api/hooks/spec-update`
7. **Verify Update**: Check `.kiro/spec.md` was modified
8. **Show Steering**: Open `.kiro/steering.md`

## 📊 Project Stats

- **Total Endpoints**: 20
- **Database Models**: 3
- **Serializers**: 8
- **Test Cases**: 8 test classes
- **Lines of Code**: ~3,000+
- **Documentation Files**: 7

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Or use SQLite (edit settings.py)
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Module Not Found
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 📝 License

MIT License - See LICENSE file

## 👥 Team

Backend Engineer: Mad Scientist 🧪

## 🔗 Links

- **API Docs**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **GitHub**: [Repository URL]
- **Devpost**: [Submission URL]

---

Built with ❤️ for Kiroween Hackathon 🎃
