"""
URL routing for API endpoints
"""
from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health', views.health_check, name='health'),
    
    # Authentication
    path('auth/register', views.register_view, name='register'),
    path('auth/login', views.login_view, name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('auth/refresh', views.refresh_token_view, name='refresh-token'),
    path('auth/profile', views.user_profile_view, name='user-profile'),
    path('auth/profile/update', views.update_profile_view, name='update-profile'),
    
    # Conversations
    path('conversations', views.list_conversations, name='list-conversations'),
    path('conversations/create', views.create_conversation, name='create-conversation'),
    path('conversations/<uuid:conversation_id>', views.get_conversation, name='get-conversation'),
    path('conversations/<uuid:conversation_id>/update', views.update_conversation, name='update-conversation'),
    path('conversations/<uuid:conversation_id>/delete', views.delete_conversation, name='delete-conversation'),
    
    # Chat
    path('chat', views.chat_view, name='chat'),
    
    # MCP Endpoints
    path('mcp/remember', views.mcp_remember, name='mcp-remember'),
    path('mcp/search', views.mcp_search, name='mcp-search'),
    path('mcp/inject', views.mcp_inject, name='mcp-inject'),
    path('mcp/listMemories', views.mcp_list_memories, name='mcp-list-memories'),
    path('mcp/memory/<int:memory_id>/delete', views.delete_memory, name='delete-memory'),
    path('mcp/conversation/<str:conversation_id>/clear', views.clear_conversation_memories, name='clear-memories'),
    
    # Hooks
    path('hooks/spec-update', views.spec_hook, name='spec-hook'),
]
