# Chimera Protocol - Documentation Index

Quick navigation to all project documentation.

## 🚀 Getting Started

| Document | Purpose | Time |
|----------|---------|------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get running in 5 minutes | 5 min |
| **[README.md](README.md)** | Complete project documentation | 15 min |
| **[STATUS.md](STATUS.md)** | Current project status | 5 min |

## 📚 Core Documentation

### Setup & Installation
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
- **[README.md](README.md)** - Detailed setup instructions
- **setup.sh** / **setup.bat** - Automated setup scripts
- **run.sh** / **run.bat** - Run scripts
- **Makefile** - Make commands

### API Documentation
- **[README.md#api-documentation](README.md#-api-documentation)** - API reference
- **http://localhost:8000/swagger/** - Interactive API docs (when running)
- **http://localhost:8000/redoc/** - ReDoc documentation (when running)
- **[.kiro/spec.md](.kiro/spec.md)** - API specification

### Testing
- **[README.md#testing](README.md#-testing)** - Testing guide
- **test_api.sh** - API testing script
- **verify_setup.py** - Setup verification
- **api/tests.py** - Unit tests

## 🎯 Kiro Features

### Spec-Driven Development
- **[.kiro/spec.md](.kiro/spec.md)** - Complete API specification
- **[HOW_WE_USED_KIRO.md#1-spec-driven-development](HOW_WE_USED_KIRO.md#1--spec-driven-development)** - How we used it

### Agent Hooks
- **[HOW_WE_USED_KIRO.md#2-agent-hooks](HOW_WE_USED_KIRO.md#2--agent-hooks)** - Implementation details
- **api/views.py** - `spec_hook()` function

### MCP Protocol
- **[HOW_WE_USED_KIRO.md#3-mcp-model-context-protocol](HOW_WE_USED_KIRO.md#3--mcp-model-context-protocol)** - Full explanation
- **api/memory_service.py** - Vector search implementation
- **api/views.py** - MCP endpoints

### Steering Documents
- **[.kiro/steering.md](.kiro/steering.md)** - Coding guidelines
- **[HOW_WE_USED_KIRO.md#4-steering-documents](HOW_WE_USED_KIRO.md#4--steering-documents)** - How we used it

## 🚢 Deployment

### Deployment Guides
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Complete deployment guide
- **[README.md#-deployment](README.md#-deployment)** - Quick deploy options

### Platform-Specific
- **[DEPLOYMENT_CHECKLIST.md#option-1-railway](DEPLOYMENT_CHECKLIST.md#option-1-railway-recommended---fastest)** - Railway
- **[DEPLOYMENT_CHECKLIST.md#option-2-render](DEPLOYMENT_CHECKLIST.md#option-2-render)** - Render
- **[DEPLOYMENT_CHECKLIST.md#option-3-heroku](DEPLOYMENT_CHECKLIST.md#option-3-heroku)** - Heroku
- **[DEPLOYMENT_CHECKLIST.md#option-4-digitalocean](DEPLOYMENT_CHECKLIST.md#option-4-digitalocean-app-platform)** - DigitalOcean

## 📊 Project Information

### Overview
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project summary
- **[HOW_WE_USED_KIRO.md](HOW_WE_USED_KIRO.md)** - Kiro features explanation
- **[STATUS.md](STATUS.md)** - Current status & metrics

### Technical Details
- **[README.md#-project-structure](README.md#-project-structure)** - Code organization
- **[PROJECT_SUMMARY.md#-technology-stack](PROJECT_SUMMARY.md#-technology-stack)** - Tech stack
- **[PROJECT_SUMMARY.md#-database-models](PROJECT_SUMMARY.md#-database-models)** - Data models

## 🎬 Demo & Presentation

### Demo Resources
- **[README.md#-demo-script](README.md#-demo-script)** - Demo workflow
- **[HOW_WE_USED_KIRO.md#-complete-demo-flow](HOW_WE_USED_KIRO.md#-complete-demo-flow)** - Detailed demo
- **test_api.sh** - Automated demo script

### Submission
- **[DEPLOYMENT_CHECKLIST.md#-devpost-submission](DEPLOYMENT_CHECKLIST.md#-devpost-submission)** - Submission guide
- **[HOW_WE_USED_KIRO.md#-hackathon-judging-points](HOW_WE_USED_KIRO.md#-hackathon-judging-points)** - Judging criteria

## 🔧 Configuration

### Environment
- **.env.example** - Environment template
- **[README.md#-configuration](README.md#-configuration)** - Configuration guide
- **chimera/settings.py** - Django settings

### Database
- **[QUICKSTART.md#step-1-database-setup](QUICKSTART.md#step-1-database-setup-2-min)** - Database setup
- **[README.md#database-setup](README.md#database-setup)** - Detailed DB config

## 📝 Code Reference

### Models
- **api/models.py** - Database models
  - Memory
  - Conversation
  - ChatMessage

### Views
- **api/views.py** - API endpoints
  - health_check
  - login_view
  - mcp_remember
  - mcp_search
  - mcp_inject
  - mcp_list_memories
  - chat_view
  - spec_hook

### Serializers
- **api/serializers.py** - DRF serializers
  - MemorySerializer
  - RememberSerializer
  - SearchSerializer
  - InjectSerializer
  - ChatSerializer
  - SpecHookSerializer

### Services
- **api/memory_service.py** - Memory service
  - MemoryService class
  - TF-IDF search
  - Cosine similarity

## 🧪 Testing

### Test Files
- **api/tests.py** - Unit tests
- **test_api.sh** - API integration tests
- **verify_setup.py** - Setup verification

### Running Tests
```bash
# Unit tests
python manage.py test

# API tests
./test_api.sh

# Setup verification
python verify_setup.py
```

## 🐛 Troubleshooting

### Common Issues
- **[QUICKSTART.md#-troubleshooting](QUICKSTART.md#-troubleshooting)** - Quick fixes
- **[README.md#troubleshooting](README.md#troubleshooting)** - Detailed solutions
- **[DEPLOYMENT_CHECKLIST.md#-support](DEPLOYMENT_CHECKLIST.md#-support)** - Deployment issues

## 📄 Legal & License

- **[LICENSE](LICENSE)** - MIT License
- **[README.md#-license](README.md#-license)** - License info

## 🔗 Quick Links

### Local Development
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### External Resources
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/

## 📋 Checklists

### Setup Checklist
- [ ] Read QUICKSTART.md
- [ ] Run setup script
- [ ] Configure .env
- [ ] Run migrations
- [ ] Create superuser
- [ ] Start server
- [ ] Test endpoints

### Deployment Checklist
- [ ] Read DEPLOYMENT_CHECKLIST.md
- [ ] Choose platform
- [ ] Configure production settings
- [ ] Deploy application
- [ ] Run migrations
- [ ] Test deployed endpoints
- [ ] Update documentation

### Submission Checklist
- [ ] Code complete
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Deployed and accessible
- [ ] Demo video recorded
- [ ] Screenshots taken
- [ ] Devpost submission ready

## 🎯 By Role

### For Developers
1. [QUICKSTART.md](QUICKSTART.md) - Get started
2. [README.md](README.md) - Full documentation
3. **api/** - Source code
4. **api/tests.py** - Tests

### For Judges
1. [HOW_WE_USED_KIRO.md](HOW_WE_USED_KIRO.md) - Kiro features
2. [.kiro/spec.md](.kiro/spec.md) - API spec
3. [.kiro/steering.md](.kiro/steering.md) - Guidelines
4. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Overview

### For DevOps
1. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deploy guide
2. **requirements.txt** - Dependencies
3. **.env.example** - Configuration
4. **chimera/settings.py** - Settings

### For Users
1. [QUICKSTART.md](QUICKSTART.md) - Quick start
2. **http://localhost:8000/swagger/** - API docs
3. [README.md#api-documentation](README.md#-api-documentation) - API reference

## 📊 Document Statistics

- **Total Documents**: 10+
- **Setup Guides**: 3
- **API Documentation**: 4
- **Kiro Documentation**: 3
- **Deployment Guides**: 1
- **Testing Guides**: 3

## 🎉 Quick Commands

```bash
# Setup
./setup.sh              # Linux/Mac
setup.bat               # Windows

# Run
./run.sh                # Linux/Mac
run.bat                 # Windows
python manage.py runserver

# Test
python verify_setup.py
./test_api.sh
python manage.py test

# Deploy
# See DEPLOYMENT_CHECKLIST.md
```

---

**Need help?** Start with [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)

**Ready to deploy?** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**Want to understand Kiro features?** Read [HOW_WE_USED_KIRO.md](HOW_WE_USED_KIRO.md)

---

**Project**: Chimera Protocol  
**Status**: Complete  
**Documentation**: Comprehensive  
**Ready**: ✅ Demo, Deploy, Submit
