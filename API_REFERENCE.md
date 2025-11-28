# Chimera Protocol - Complete API Reference

## Base URL
```
http://localhost:8000/api/
```

## Response Format
All endpoints return JSON with this envelope:
```json
{
  "ok": boolean,
  "data": object | array | null,
  "error": string | null
}
```

---

## 1. Health & Status

### Health Check
Check API and database status.

**Endpoint**: `GET /api/health`  
**Authentication**: None

**Response**:
```json
{
  "ok": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "database": "connected"
  },
  "error": null
}
```

---

## 2. Authentication

### Register User
Create a new user account.

**Endpoint**: `POST /api/auth/register`  
**Authentication**: None

**Request**:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response** (201 Created):
```json
{
  "ok": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user_id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "error": null
}
```

### Login
Authenticate user and receive JWT tokens.

**Endpoint**: `POST /api/auth/login`  
**Authentication**: None

**Request**:
```json
{
  "username": "john",
  "password": "securepass123"
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user_id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "error": null
}
```

### Logout
Blacklist refresh token.

**Endpoint**: `POST /api/auth/logout`  
**Authentication**: Required (Bearer token)

**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "message": "Successfully logged out"
  },
  "error": null
}
```

### Refresh Token
Get new access token using refresh token.

**Endpoint**: `POST /api/auth/refresh`  
**Authentication**: None

**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "error": null
}
```

### Get Profile
Get current user profile.

**Endpoint**: `GET /api/auth/profile`  
**Authentication**: Required

**Response**:
```json
{
  "ok": true,
  "data": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  },
  "error": null
}
```

### Update Profile
Update user profile information.

**Endpoint**: `PUT /api/auth/profile/update`  
**Authentication**: Required

**Request**:
```json
{
  "email": "newemail@example.com"
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "id": 1,
    "username": "john",
    "email": "newemail@example.com"
  },
  "error": null
}
```

---

## 3. Conversations

### List Conversations
Get all conversations for authenticated user.

**Endpoint**: `GET /api/conversations`  
**Authentication**: Required

**Response**:
```json
{
  "ok": true,
  "data": {
    "conversations": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "My Conversation",
        "message_count": 5,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T01:00:00Z"
      }
    ],
    "total": 1
  },
  "error": null
}
```

### Create Conversation
Create a new conversation.

**Endpoint**: `POST /api/conversations/create`  
**Authentication**: Required

**Request**:
```json
{
  "title": "New Conversation"
}
```

**Response** (201 Created):
```json
{
  "ok": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "New Conversation",
    "message_count": 0,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "error": null
}
```

### Get Conversation
Get conversation details with all messages.

**Endpoint**: `GET /api/conversations/{conversation_id}`  
**Authentication**: Required

**Response**:
```json
{
  "ok": true,
  "data": {
    "conversation": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "My Conversation",
      "message_count": 2,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T01:00:00Z"
    },
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "Hello!",
        "metadata": {},
        "created_at": "2024-01-01T00:00:00Z"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Hi there!",
        "metadata": {},
        "created_at": "2024-01-01T00:01:00Z"
      }
    ]
  },
  "error": null
}
```

### Update Conversation
Update conversation title.

**Endpoint**: `PUT /api/conversations/{conversation_id}/update`  
**Authentication**: Required

**Request**:
```json
{
  "title": "Updated Title"
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Updated Title",
    "message_count": 2,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T02:00:00Z"
  },
  "error": null
}
```

### Delete Conversation
Delete conversation and all its messages.

**Endpoint**: `DELETE /api/conversations/{conversation_id}/delete`  
**Authentication**: Required

**Response**:
```json
{
  "ok": true,
  "data": {
    "message": "Conversation deleted successfully"
  },
  "error": null
}
```

---

## 4. Chat

### Chat
Send a message and optionally store in memory.

**Endpoint**: `POST /api/chat`  
**Authentication**: None

**Request**:
```json
{
  "conversation_id": "conv-123",
  "message": "What's the weather like?",
  "model": "gpt-3.5-turbo",
  "remember": true
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "reply": "Echo: What's the weather like?",
    "trace": {
      "model": "gpt-3.5-turbo",
      "conversation_id": "conv-123",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    "memory_injected": true
  },
  "error": null
}
```

---

## 5. MCP (Memory) Operations

### Remember
Store a memory fragment.

**Endpoint**: `POST /api/mcp/remember`  
**Authentication**: None

**Request**:
```json
{
  "text": "User prefers Python programming",
  "tags": ["preference", "programming"],
  "conversation_id": "conv-123",
  "metadata": {
    "source": "chat",
    "importance": "high"
  }
}
```

**Response** (201 Created):
```json
{
  "ok": true,
  "data": {
    "id": 1,
    "status": "saved",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "error": null
}
```

### Search
Search memories using semantic similarity.

**Endpoint**: `POST /api/mcp/search`  
**Authentication**: None

**Request**:
```json
{
  "query": "programming languages",
  "top_k": 5,
  "conversation_id": "conv-123"
}
```

**Response**:
```json
{
  "ok": true,
  "data": [
    {
      "id": 1,
      "text": "User prefers Python programming",
      "score": 0.85,
      "tags": ["preference", "programming"],
      "conversation_id": "conv-123",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "text": "User is learning JavaScript",
      "score": 0.72,
      "tags": ["learning", "programming"],
      "conversation_id": "conv-123",
      "created_at": "2024-01-01T00:05:00Z"
    }
  ],
  "error": null
}
```

### Inject Context
Get formatted context from recent memories.

**Endpoint**: `POST /api/mcp/inject`  
**Authentication**: None

**Request**:
```json
{
  "conversation_id": "conv-123",
  "max_memories": 10
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "injected_context": "- User prefers Python programming\n- User is learning JavaScript\n- User likes dark mode",
    "memory_count": 3,
    "memories": [
      {
        "id": 1,
        "text": "User prefers Python programming",
        "tags": ["preference"],
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  },
  "error": null
}
```

### List Memories
Get paginated list of memories for a conversation.

**Endpoint**: `GET /api/mcp/listMemories?conversation_id={id}&limit={n}&offset={n}`  
**Authentication**: None

**Query Parameters**:
- `conversation_id` (required): Conversation ID
- `limit` (optional, default: 20): Number of results
- `offset` (optional, default: 0): Pagination offset

**Response**:
```json
{
  "ok": true,
  "data": {
    "memories": [
      {
        "id": 1,
        "text": "User prefers Python",
        "tags": ["preference"],
        "conversation_id": "conv-123",
        "metadata": {},
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 10,
    "limit": 20,
    "offset": 0
  },
  "error": null
}
```

### Delete Memory
Delete a specific memory by ID.

**Endpoint**: `DELETE /api/mcp/memory/{memory_id}/delete`  
**Authentication**: None

**Response**:
```json
{
  "ok": true,
  "data": {
    "message": "Memory deleted successfully"
  },
  "error": null
}
```

### Clear Conversation Memories
Delete all memories for a conversation.

**Endpoint**: `DELETE /api/mcp/conversation/{conversation_id}/clear`  
**Authentication**: None

**Response**:
```json
{
  "ok": true,
  "data": {
    "message": "Deleted 5 memories",
    "count": 5
  },
  "error": null
}
```

---

## 6. Agent Hooks

### Spec Update Hook
Auto-append new endpoint definition to spec.md.

**Endpoint**: `POST /api/hooks/spec-update`  
**Authentication**: None

**Request**:
```json
{
  "type": "endpoint",
  "path": "/api/new-feature",
  "method": "POST",
  "description": "New feature endpoint",
  "schema": {
    "request": {
      "field": "string"
    },
    "response": {
      "result": "string"
    }
  }
}
```

**Response**:
```json
{
  "ok": true,
  "data": {
    "status": "ok",
    "updated": true,
    "message": "Spec updated successfully"
  },
  "error": null
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "ok": false,
  "data": null,
  "error": "Error message here"
}
```

### Common HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Authentication

For endpoints requiring authentication, include JWT token in header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## Rate Limiting

Currently no rate limiting implemented. Recommended for production:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## Pagination

List endpoints support pagination via query parameters:
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Starting position (default: 0)

Example:
```
GET /api/mcp/listMemories?conversation_id=conv-123&limit=10&offset=20
```

---

## Complete Endpoint Summary

| # | Endpoint | Method | Auth | Purpose |
|---|----------|--------|------|---------|
| 1 | `/api/health` | GET | No | Health check |
| 2 | `/api/auth/register` | POST | No | Register user |
| 3 | `/api/auth/login` | POST | No | Login user |
| 4 | `/api/auth/logout` | POST | Yes | Logout user |
| 5 | `/api/auth/refresh` | POST | No | Refresh token |
| 6 | `/api/auth/profile` | GET | Yes | Get profile |
| 7 | `/api/auth/profile/update` | PUT | Yes | Update profile |
| 8 | `/api/conversations` | GET | Yes | List conversations |
| 9 | `/api/conversations/create` | POST | Yes | Create conversation |
| 10 | `/api/conversations/{id}` | GET | Yes | Get conversation |
| 11 | `/api/conversations/{id}/update` | PUT | Yes | Update conversation |
| 12 | `/api/conversations/{id}/delete` | DELETE | Yes | Delete conversation |
| 13 | `/api/chat` | POST | No | Chat |
| 14 | `/api/mcp/remember` | POST | No | Store memory |
| 15 | `/api/mcp/search` | POST | No | Search memories |
| 16 | `/api/mcp/inject` | POST | No | Inject context |
| 17 | `/api/mcp/listMemories` | GET | No | List memories |
| 18 | `/api/mcp/memory/{id}/delete` | DELETE | No | Delete memory |
| 19 | `/api/mcp/conversation/{id}/clear` | DELETE | No | Clear memories |
| 20 | `/api/hooks/spec-update` | POST | No | Update spec |

---

**Total Endpoints**: 20  
**Documentation Version**: 1.0  
**Last Updated**: 2024
