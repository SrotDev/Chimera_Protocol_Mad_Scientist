"""
API Views for Chimera Protocol
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json
import os

from .models import Memory, Conversation, ChatMessage
from .serializers import (
    MemorySerializer, RememberSerializer, SearchSerializer,
    InjectSerializer, ChatSerializer, SpecHookSerializer,
    ConversationSerializer, UserSerializer, ChatMessageSerializer
)
from .memory_service import memory_service


def api_response(ok=True, data=None, error=None):
    """
    Standard API response envelope
    """
    return {
        'ok': ok,
        'data': data,
        'error': error
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint
    """
    try:
        # Check database connection
        Memory.objects.count()
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return Response(api_response(
        ok=True,
        data={
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'database': db_status
        }
    ))


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    User registration endpoint
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            api_response(ok=False, error='Username and password required'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        return Response(
            api_response(ok=False, error='Username already exists'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if email and User.objects.filter(email=email).exists():
        return Response(
            api_response(ok=False, error='Email already exists'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email or '',
            password=password
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(api_response(
            ok=True,
            data={
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }
        ), status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            api_response(ok=False, error='Username and password required'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            api_response(ok=False, error='Invalid credentials'),
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    
    return Response(api_response(
        ok=True,
        data={
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
    ))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint - blacklist refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response(api_response(
            ok=True,
            data={'message': 'Successfully logged out'}
        ))
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    Refresh access token using refresh token
    """
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            api_response(ok=False, error='Refresh token required'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        
        return Response(api_response(
            ok=True,
            data={
                'token': str(refresh.access_token)
            }
        ))
    except Exception as e:
        return Response(
            api_response(ok=False, error='Invalid or expired refresh token'),
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(api_response(
        ok=True,
        data=serializer.data
    ))


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    Update user profile
    """
    user = request.user
    
    email = request.data.get('email')
    if email:
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return Response(
                api_response(ok=False, error='Email already in use'),
                status=status.HTTP_400_BAD_REQUEST
            )
        user.email = email
    
    user.save()
    serializer = UserSerializer(user)
    
    return Response(api_response(
        ok=True,
        data=serializer.data
    ))


@api_view(['POST'])
@permission_classes([AllowAny])
def mcp_remember(request):
    """
    MCP Remember endpoint - Store a memory
    """
    serializer = RememberSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            api_response(ok=False, error=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = serializer.validated_data
        
        # Create memory
        memory = Memory.objects.create(
            text=data['text'],
            tags=data.get('tags', []),
            conversation_id=data['conversation_id'],
            metadata=data.get('metadata', {})
        )
        
        # Store in search service
        memory_service.store(memory.text, memory.id)
        
        return Response(api_response(
            ok=True,
            data={
                'id': memory.id,
                'status': 'saved',
                'created_at': memory.created_at.isoformat()
            }
        ), status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def mcp_search(request):
    """
    MCP Search endpoint - Search memories by similarity
    """
    serializer = SearchSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            api_response(ok=False, error=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = serializer.validated_data
        query = data['query']
        top_k = data.get('top_k', 5)
        conversation_id = data.get('conversation_id')
        
        # Search using memory service
        results = memory_service.search(query, top_k, conversation_id)
        
        return Response(api_response(
            ok=True,
            data=results
        ))
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def mcp_inject(request):
    """
    MCP Inject endpoint - Get relevant memories for context injection
    """
    serializer = InjectSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            api_response(ok=False, error=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = serializer.validated_data
        conversation_id = data['conversation_id']
        max_memories = data.get('max_memories', 10)
        
        # Get recent memories for this conversation
        memories = Memory.objects.filter(
            conversation_id=conversation_id
        ).order_by('-created_at')[:max_memories]
        
        # Format as context
        context_parts = []
        memory_list = []
        
        for memory in memories:
            context_parts.append(f"- {memory.text}")
            memory_list.append({
                'id': memory.id,
                'text': memory.text,
                'tags': memory.tags,
                'created_at': memory.created_at.isoformat()
            })
        
        injected_context = "\n".join(context_parts) if context_parts else "No previous memories found."
        
        return Response(api_response(
            ok=True,
            data={
                'injected_context': injected_context,
                'memory_count': len(memory_list),
                'memories': memory_list
            }
        ))
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def mcp_list_memories(request):
    """
    MCP List Memories endpoint - Get paginated list of memories
    """
    conversation_id = request.query_params.get('conversation_id')
    
    if not conversation_id:
        return Response(
            api_response(ok=False, error='conversation_id is required'),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        memories = Memory.objects.filter(
            conversation_id=conversation_id
        ).order_by('-created_at')
        
        total = memories.count()
        memories_page = memories[offset:offset + limit]
        
        serializer = MemorySerializer(memories_page, many=True)
        
        return Response(api_response(
            ok=True,
            data={
                'memories': serializer.data,
                'total': total,
                'limit': limit,
                'offset': offset
            }
        ))
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def chat_view(request):
    """
    Chat endpoint - Process chat message with optional memory storage
    """
    serializer = ChatSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            api_response(ok=False, error=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = serializer.validated_data
        conversation_id = data['conversation_id']
        message = data['message']
        remember = data.get('remember', False)
        
        # Simple echo response (replace with actual AI integration)
        reply = f"Echo: {message}"
        
        # Store in memory if requested
        memory_injected = False
        if remember:
            Memory.objects.create(
                text=f"User: {message}",
                conversation_id=conversation_id,
                tags=['chat', 'user_message']
            )
            Memory.objects.create(
                text=f"Assistant: {reply}",
                conversation_id=conversation_id,
                tags=['chat', 'assistant_response']
            )
            memory_injected = True
        
        return Response(api_response(
            ok=True,
            data={
                'reply': reply,
                'trace': {
                    'model': data.get('model', 'echo'),
                    'conversation_id': conversation_id,
                    'timestamp': timezone.now().isoformat()
                },
                'memory_injected': memory_injected
            }
        ))
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_conversations(request):
    """
    List all conversations for the authenticated user
    """
    conversations = Conversation.objects.filter(user=request.user)
    serializer = ConversationSerializer(conversations, many=True)
    
    return Response(api_response(
        ok=True,
        data={
            'conversations': serializer.data,
            'total': conversations.count()
        }
    ))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_conversation(request):
    """
    Create a new conversation
    """
    title = request.data.get('title', 'New Conversation')
    
    conversation = Conversation.objects.create(
        user=request.user,
        title=title
    )
    
    serializer = ConversationSerializer(conversation)
    
    return Response(api_response(
        ok=True,
        data=serializer.data
    ), status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, conversation_id):
    """
    Get a specific conversation with messages
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        messages = conversation.messages.all()
        
        conversation_data = ConversationSerializer(conversation).data
        messages_data = ChatMessageSerializer(messages, many=True).data
        
        return Response(api_response(
            ok=True,
            data={
                'conversation': conversation_data,
                'messages': messages_data
            }
        ))
    except Conversation.DoesNotExist:
        return Response(
            api_response(ok=False, error='Conversation not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_conversation(request, conversation_id):
    """
    Update conversation title
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        
        title = request.data.get('title')
        if title:
            conversation.title = title
            conversation.save()
        
        serializer = ConversationSerializer(conversation)
        
        return Response(api_response(
            ok=True,
            data=serializer.data
        ))
    except Conversation.DoesNotExist:
        return Response(
            api_response(ok=False, error='Conversation not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_conversation(request, conversation_id):
    """
    Delete a conversation and all its messages
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        conversation.delete()
        
        return Response(api_response(
            ok=True,
            data={'message': 'Conversation deleted successfully'}
        ))
    except Conversation.DoesNotExist:
        return Response(
            api_response(ok=False, error='Conversation not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_memory(request, memory_id):
    """
    Delete a specific memory
    """
    try:
        memory = Memory.objects.get(id=memory_id)
        memory.delete()
        
        return Response(api_response(
            ok=True,
            data={'message': 'Memory deleted successfully'}
        ))
    except Memory.DoesNotExist:
        return Response(
            api_response(ok=False, error='Memory not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_conversation_memories(request, conversation_id):
    """
    Clear all memories for a conversation
    """
    deleted_count = Memory.objects.filter(conversation_id=conversation_id).delete()[0]
    
    return Response(api_response(
        ok=True,
        data={
            'message': f'Deleted {deleted_count} memories',
            'count': deleted_count
        }
    ))


@api_view(['POST'])
@permission_classes([AllowAny])
def spec_hook(request):
    """
    Spec Hook endpoint - Auto-update spec.md with new endpoint definitions
    """
    serializer = SpecHookSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            api_response(ok=False, error=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        data = serializer.validated_data
        
        # Path to spec.md
        spec_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.kiro', 'spec.md')
        
        # Format new endpoint entry
        new_entry = f"\n\n## Hook-Added Endpoint\n"
        new_entry += f"- **{data['method']}** `{data['path']}`\n"
        if data.get('description'):
            new_entry += f"  - Description: {data['description']}\n"
        if data.get('schema'):
            new_entry += f"  - Schema: ```json\n{json.dumps(data['schema'], indent=2)}\n```\n"
        new_entry += f"  - Type: {data['type']}\n"
        new_entry += f"  - Added: {timezone.now().isoformat()}\n"
        
        # Append to spec.md
        with open(spec_path, 'a', encoding='utf-8') as f:
            f.write(new_entry)
        
        return Response(api_response(
            ok=True,
            data={
                'status': 'ok',
                'updated': True,
                'message': 'Spec updated successfully'
            }
        ))
        
    except Exception as e:
        return Response(
            api_response(ok=False, error=str(e)),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
