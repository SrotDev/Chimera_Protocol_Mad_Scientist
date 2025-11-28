# Chimera Backend Steering Rules

## Coding Style
- **Framework**: Django REST Framework
- **Naming**: snake_case for variables, functions, and file names
- **Documentation**: All functions must have docstrings
- **Response Format**: Always return JSON envelope `{ok: boolean, data: any, error: string|null}`
- **Error Handling**: Use try-except blocks, return meaningful error messages
- **Type Hints**: Use Python type hints where applicable

## Memory Management Rules
- **Text Chunking**: Chunk text to < 500 tokens before storage
- **Conversation ID**: Always store and index by conversation_id
- **Embeddings**: Compute TF-IDF embeddings on remember operations
- **Search**: Use cosine similarity for vector search
- **Cleanup**: Implement soft deletes, keep audit trail

## Database
- **Primary DB**: PostgreSQL
- **Migrations**: Always create migrations for model changes
- **Indexing**: Index frequently queried fields (conversation_id, created_at)
- **JSON Fields**: Use PostgreSQL JSON fields for flexible metadata

## API Design
- **Versioning**: Prefix all endpoints with `/api/`
- **HTTP Methods**: Follow REST conventions (GET, POST, PUT, DELETE)
- **Status Codes**: Use appropriate HTTP status codes
- **Pagination**: Implement pagination for list endpoints (limit, offset)
- **CORS**: Enable CORS for frontend integration

## Security
- **Authentication**: Token-based auth (JWT or DRF tokens)
- **Validation**: Validate all input data using serializers
- **SQL Injection**: Use ORM, never raw SQL with user input
- **Rate Limiting**: Implement rate limiting on public endpoints

## Testing
- **Unit Tests**: Test all views and models
- **Integration Tests**: Test API endpoints end-to-end
- **Coverage**: Aim for >80% code coverage

## MCP Protocol
- **Consistency**: Follow MCP specification for memory operations
- **Metadata**: Store rich metadata with each memory
- **Context Window**: Limit injected context to reasonable size (4000 tokens)
- **Relevance**: Return most relevant memories based on similarity score
