# Chimera Backend Spec v1

## Overview
Spec-driven backend for Kiroween - A conversational AI with persistent memory using MCP (Model Context Protocol).

## Authentication

### Register
- **POST** `/api/auth/register`
  - Request: `{username: string, email?: string, password: string}`
  - Response: `{token: string, refresh: string, user_id: string, username: string, email: string}`
  - Description: Create a new user account

### Login
- **POST** `/api/auth/login`
  - Request: `{username: string, password: string}`
  - Response: `{token: string, refresh: string, user_id: string, username: string, email: string}`
  - Description: Authenticate user and receive JWT tokens

### Logout
- **POST** `/api/auth/logout`
  - Request: `{refresh: string}`
  - Response: `{message: string}`
  - Description: Blacklist refresh token (requires authentication)

### Refresh Token
- **POST** `/api/auth/refresh`
  - Request: `{refresh: string}`
  - Response: `{token: string}`
  - Description: Get new access token using refresh token

### Get Profile
- **GET** `/api/auth/profile`
  - Response: `{id: string, username: string, email: string}`
  - Description: Get current user profile (requires authentication)

### Update Profile
- **PUT** `/api/auth/profile/update`
  - Request: `{email?: string}`
  - Response: `{id: string, username: string, email: string}`
  - Description: Update user profile (requires authentication)

## Conversations

### List Conversations
- **GET** `/api/conversations`
  - Response: `{conversations: array, total: number}`
  - Description: List all conversations for authenticated user (requires authentication)

### Create Conversation
- **POST** `/api/conversations/create`
  - Request: `{title?: string}`
  - Response: `{id: uuid, title: string, created_at: string, updated_at: string}`
  - Description: Create a new conversation (requires authentication)

### Get Conversation
- **GET** `/api/conversations/{conversation_id}`
  - Response: `{conversation: object, messages: array}`
  - Description: Get conversation details with all messages (requires authentication)

### Update Conversation
- **PUT** `/api/conversations/{conversation_id}/update`
  - Request: `{title: string}`
  - Response: `{id: uuid, title: string, updated_at: string}`
  - Description: Update conversation title (requires authentication)

### Delete Conversation
- **DELETE** `/api/conversations/{conversation_id}/delete`
  - Response: `{message: string}`
  - Description: Delete conversation and all messages (requires authentication)

## Chat Pipeline
- **POST** `/api/chat`
  - Request: `{conversation_id: string, message: string, model?: string, remember?: boolean}`
  - Response: `{reply: string, trace: object, memory_injected: boolean}`
  - Description: Main chat endpoint. Optionally stores conversation in memory if `remember=true`

## Memory Storage (MCP Endpoints)

### Remember
- **POST** `/api/mcp/remember`
  - Request: `{text: string, tags?: string[], conversation_id: string, metadata?: object}`
  - Response: `{id: number, status: string, created_at: string}`
  - Description: Store a memory fragment with optional tags

### Search
- **POST** `/api/mcp/search`
  - Request: `{query: string, top_k?: number, conversation_id?: string}`
  - Response: `[{id: number, text: string, score: float, tags: string[], created_at: string}]`
  - Description: Vector search over stored memories using TF-IDF similarity

### Inject Context
- **POST** `/api/mcp/inject`
  - Request: `{conversation_id: string, max_memories?: number}`
  - Response: `{injected_context: string, memory_count: number, memories: array}`
  - Description: Retrieve and format relevant memories for conversation context

### List Memories
- **GET** `/api/mcp/listMemories`
  - Query Params: `conversation_id` (required), `limit` (optional), `offset` (optional)
  - Response: `{memories: [{id, text, tags, created_at}], total: number}`
  - Description: Paginated list of memories for a conversation

### Delete Memory
- **DELETE** `/api/mcp/memory/{memory_id}/delete`
  - Response: `{message: string}`
  - Description: Delete a specific memory by ID

### Clear Conversation Memories
- **DELETE** `/api/mcp/conversation/{conversation_id}/clear`
  - Response: `{message: string, count: number}`
  - Description: Delete all memories for a specific conversation

## Agent Hooks

### Spec Update Hook
- **POST** `/api/hooks/spec-update`
  - Request: `{type: string, path: string, method: string, schema?: object, description?: string}`
  - Response: `{status: string, updated: boolean}`
  - Description: Auto-append new endpoint specs to .kiro/spec.md

## Admin & Health

### Health Check
- **GET** `/health`
  - Response: `{status: string, timestamp: string, database: string}`
  - Description: Service health status

## Data Models

### Memory
```python
{
  id: integer (primary key),
  text: text (required),
  tags: json (array of strings),
  conversation_id: string (indexed),
  embedding: binary (optional, for vector storage),
  metadata: json (optional),
  created_at: timestamp,
  updated_at: timestamp
}
```

### Conversation
```python
{
  id: string (primary key),
  user_id: string,
  title: string,
  created_at: timestamp,
  updated_at: timestamp
}
```

## Response Format
All endpoints return JSON with consistent envelope:
```json
{
  "ok": boolean,
  "data": object | array,
  "error": string | null
}
```
