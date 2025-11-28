Love the energy, mad scientist — let’s surgically finish the **backend** for Kiroween in one day. I’ll give you a tight, executable, minute-by-minute plan (with concrete commands, file names, endpoints, and deliverables). This plan assumes you’ll use **Django + Django REST Framework** (you already know it) and a small vector memory service (simple REST that talks to a vector DB or local FAISS/Weaviate stub). It’s focused on the hackathon requirements (vibe coding, agent hooks, spec-driven, MCP) so judges can verify backend work. Key requirements from the hackathon and Kiro guidance are noted.  

---

# One-Day Backend Sprint — summary (deliverables)

* Working API server (Django) with auth, `/chat`, `/store`, `/search`, `/inject`, `/listMemories`, `/regenUI`.
* `.kiro/spec.md` and `/.kiro` directory populated from spec.
* Minimal vector-memory service (in-process FAISS or stub) with REST endpoints.
* Simple MCP endpoints (POST `/mcp/remember`, `/mcp/search`, etc.) and doc explaining them.
* Git commits + public repo with OSI license.
* Short demo instructions & credentials, and a README that shows where Kiro hooks in. (Video demo later — show endpoints & hooks firing.)

---

# Time blocks (total ≈ 10–12 hours). If you have less time, skip extras in Step 7.

### 0. Prep (15 min)

* Create repo, branch, license, and basic README.

```bash
mkdir chimera-backend && cd chimera-backend
git init
echo "# Chimera Protocol — backend" > README.md
echo "MIT" > LICENSE
git add . && git commit -m "init: repo"
gh repo create <yourname>/chimera-backend --public  # or create manually
```

* Create `.kiro` folder and initial `/.kiro/spec.md` (required by hackathon). Add a short note: “Spec-driven backend for Kiroween.” Judges require `.kiro` present. 

---

### 1. Create spec (45 min) — **SPEC-FIRST**

Create `/.kiro/spec.md` with endpoints, payloads, and model definitions. Paste this template and edit:

```
# Chimera Backend Spec v1
## Auth
POST /api/auth/login {username,password} -> {token}
## Chat pipeline
POST /api/chat {conversation_id, message, model} -> {reply, trace}
## Memory storage (MCP)
POST /api/mcp/remember {text, tags, conversation_id} -> {id, status}
POST /api/mcp/search {query, top_k} -> [{id, text, score}]
POST /api/mcp/inject {conversation_id} -> {injected_context}
GET  /api/mcp/listMemories?conversation_id=... -> [{id, text, tags}]
## Admin
GET /health -> 200
```

* Commit: `git add .kiro/spec.md && git commit -m "spec: add initial endpoints"`.
* Note for write-up: you used spec-driven dev and `.kiro/spec.md` is primary. 

---

### 2. Scaffold Django project & app (40 min)

Commands:

```bash
python -m venv .venv && source .venv/bin/activate
pip install django djangorestframework drf-yasg python-dotenv
django-admin startproject chimera .
python manage.py startapp api
```

Update `settings.py`: add `rest_framework`, `api` and CORS if needed.

Create `api/urls.py` and wire into `chimera/urls.py`.

Commit: `git add . && git commit -m "scaffold: django + api app"`

---

### 3. Implement core endpoints (2.5 hours)

Implement minimal, testable views and serializers.

Files to create:

* `api/serializers.py` — `ChatSerializer`, `RememberSerializer`, `SearchSerializer`
* `api/views.py` — implement:

  * `ChatView` (POST `/api/chat`) — accepts message, returns echo + placeholder reply; logs to memory if `remember:true`.
  * `MCPRememberView` (POST `/api/mcp/remember`) — stores memory in simple DB model.
  * `MCPListView` (GET `/api/mcp/listMemories`) — list by conversation.
  * `MCPSearchView` (POST `/api/mcp/search`) — calls vector search service (stubbed).
  * `InjectView` (POST `/api/mcp/inject`) — composes recent memories and returns as `injected_context`.
  * `HealthView` (GET `/health`).

Create simple `api/models.py`:

```py
class Memory(models.Model):
    text = models.TextField()
    tags = models.JSONField(default=list)
    conversation_id = models.CharField(max_length=128, db_index=True)
    embedding = models.BinaryField(null=True)  # optional if embedding stored externally
    created_at = models.DateTimeField(auto_now_add=True)
```

Wire URLs:

```py
path('api/chat', ChatView.as_view()),
path('api/mcp/remember', MCPRememberView.as_view()),
path('api/mcp/search', MCPSearchView.as_view()),
path('api/mcp/inject', InjectView.as_view()),
path('api/mcp/listMemories', MCPListView.as_view()),
path('health', HealthView.as_view()),
```

Unit test quick sanity (optional): add one test for `/health`.

Commit often: e.g. `git commit -m "feat: add chat and mcp endpoints + Memory model"`

---

### 4. Vector memory service (1.5 hours)

If time: add a very small vector-index service. Two options:

A) **Fast (recommended)** — stub service that returns top-N by text-similarity (cosine over TF-IDF) using scikit-learn — good enough for demo.

* New `memory_service.py` in repo:

  * `store(text, id)` → adds to in-memory list (and sqlite via Memory model)
  * `search(query, top_k)` → compute TF-IDF similarity and return top_k

B) **Extra (if you know FAISS/weaviate)** — integrate FAISS local index.

Expose a small REST wrapper in Django (`/api/memory/search`), or spin a tiny FastAPI microservice.

Commit: `git commit -m "feat: add in-process memory service (tfidf) for vector search"`

---

### 5. MCP endpoints & docs (30 min)

Implement `POST /api/mcp/remember`, `POST /api/mcp/search`, `POST /api/mcp/inject`, `GET /api/mcp/listMemories`. Add `docs/mcp.md` explaining:

* `remember(text, conversation_id)` -> calls `/api/mcp/remember`
* `search(query, top_k)` -> calls `/api/mcp/search`
* `inject(conversation_id)` -> calls `/api/mcp/inject`

This is the MCP surface Kiro will call via hooks. Document payload examples.

Commit.

---

### 6. Agent hooks & auto-spec example (45 min)

Create one simple hook simulation (not full Kiro agent hook runtime, just a demonstration file) in `hooks/auto_spec_updater.py`:

* Monitors commit messages or listens on a small webhook endpoint `/api/hooks/spec-update` that accepts payloads like `{type: "new-endpoint", path: "/api/new", method:"POST", schema: {...}}` and appends a block to `/.kiro/spec.md`.

Implement minimal endpoint:

```py
@api_view(['POST'])
def spec_hook(request):
    payload = request.data
    with open('.kiro/spec.md', 'a') as f:
        f.write("\n## Hook-added endpoint\n")
        f.write(json.dumps(payload, indent=2))
    return Response({"status":"ok"})
```

This demonstrates agent hooks auto-updating spec (required by judges). Commit: `git commit -m "feat: add spec hook to auto-append to .kiro/spec.md"`

Reference: agent hooks and auto-spec updates are required per Kiro guide. 

---

### 7. Steering doc & config (20 min)

Create `/.kiro/steering.md` with short rules:

* Coding style: Django REST API, snake_case, docstrings, return JSON envelope `{ok, data, error}`.
* Memory rules: chunk text < 500 tokens, store conversation_id, compute embedding on remember.

Commit.

---

### 8. Tests, README, run & quick local demo (40 min)

* Add `Makefile` or `run.sh`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

* In README, add:

  * How to run locally.
  * MCP endpoints list + payload examples.
  * Where `.kiro/spec.md` lives and how hooks update it.
  * Demo steps: `curl` examples to test endpoints.

Example curl tests to include in README:

```bash
curl -X POST http://localhost:8000/api/mcp/remember -H "Content-Type: application/json" -d '{"text":"Test memory","conversation_id":"conv1"}'
curl -X POST http://localhost:8000/api/mcp/search -H "Content-Type: application/json" -d '{"query":"Test", "top_k":3}'
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"conversation_id":"conv1","message":"hello"}'
```

Commit.

---

### 9. Quick deploy for judges (optional but high reward) (45–90 min)

If you can deploy quickly:

* Use Railway / Render / Fly / Heroku (fastest). Push to GitHub then deploy.
* Provide public URL in README and Devpost submission.

If deploy time is tight: record local demo screen with ngrok forwarding `localhost:8000` (ngrok free) and show endpoints in video.

---

### 10. Final checklist & push (15 min)

* Ensure `/.kiro` exists and contains `spec.md` + `steering.md`. (Hackathon requires `/ .kiro` at repo root). 
* Add short write-up: how Kiro features used:

  * Spec-first scaffolding (show `.kiro/spec.md`).
  * Agent hook demonstration (show `/api/hooks/spec-update` writing to spec).
  * MCP endpoints implemented: `/api/mcp/*`.
  * Steering doc controls code style.
  * Note: include these points in Devpost submission write-up. 
* `git add . && git commit -m "chore: final demo-ready backend + .kiro spec & hooks" && git push origin main`

---

# Minimal code snippets (paste into project)

`api/views.py` — minimal `remember`:

```py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Memory

@api_view(['POST'])
def remember(request):
    text = request.data.get('text')
    conv = request.data.get('conversation_id')
    m = Memory.objects.create(text=text, conversation_id=conv)
    # (call memory service to embed/store)
    return Response({"id": m.id, "status": "saved"})
```

`api/views.py` — `search` (tf-idf stub):

```py
@api_view(['POST'])
def search(request):
    query = request.data.get('query')
    top_k = int(request.data.get('top_k', 5))
    # naive: order by substring occurrence
    mems = Memory.objects.filter(text__icontains=query)[:top_k]
    results = [{"id":m.id,"text":m.text,"score":1.0} for m in mems]
    return Response(results)
```

---

# What to show in the 3-minute video / demo (quick script)

1. Open repo root → show `/.kiro/spec.md` (spec-driven). 
2. Trigger spec hook: `curl -X POST /api/hooks/spec-update -d '{"path":"/api/new","method":"POST"}'` → show `.kiro/spec.md` appended. (Agent hook demo.) 
3. Call `POST /api/mcp/remember` with a note, then `POST /api/mcp/search` and show returned memory. (MCP demo.) 
4. Run `POST /api/chat` with message — show response and that chat logic can auto-save to memory.
5. Show `/.kiro/steering.md` and explain how Kiro will use it to generate consistent code. 

---

# Quick tips — scoring boosts

* Make sure `/.kiro` is committed (instant disqualifier if missing). 
* Show one automated flow: speak a new requirement → hook appends spec → run scaffold (even if manual) → run endpoint. Judges want to see the chain. 
* Include a short `how-we-used-kiro.md` referencing vibe-coding for frontend (you can claim frontend generated by Kiro), agent hooks, spec-driven backend, steering docs, and MCP endpoints — tie each claim to files in repo. 
