"""
Tests for Chimera Protocol API
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Memory, Conversation


class HealthCheckTestCase(TestCase):
    """Test health check endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_health_check(self):
        """Test health endpoint returns 200"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertEqual(response.data['data']['status'], 'healthy')


class MCPRememberTestCase(TestCase):
    """Test MCP remember endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_remember_creates_memory(self):
        """Test that remember endpoint creates a memory"""
        data = {
            'text': 'Test memory content',
            'conversation_id': 'test-conv-1',
            'tags': ['test', 'demo']
        }
        response = self.client.post('/api/mcp/remember', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['ok'])
        self.assertIn('id', response.data['data'])
        
        # Verify memory was created
        memory = Memory.objects.get(id=response.data['data']['id'])
        self.assertEqual(memory.text, 'Test memory content')
        self.assertEqual(memory.conversation_id, 'test-conv-1')
    
    def test_remember_requires_text(self):
        """Test that remember endpoint requires text field"""
        data = {
            'conversation_id': 'test-conv-1'
        }
        response = self.client.post('/api/mcp/remember', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['ok'])


class MCPSearchTestCase(TestCase):
    """Test MCP search endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test memories
        Memory.objects.create(
            text='Python is a programming language',
            conversation_id='test-conv-1',
            tags=['programming']
        )
        Memory.objects.create(
            text='Django is a web framework',
            conversation_id='test-conv-1',
            tags=['web', 'framework']
        )
    
    def test_search_returns_results(self):
        """Test that search returns relevant memories"""
        data = {
            'query': 'programming',
            'top_k': 5
        }
        response = self.client.post('/api/mcp/search', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertIsInstance(response.data['data'], list)


class MCPListMemoriesTestCase(TestCase):
    """Test MCP list memories endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test memories
        for i in range(5):
            Memory.objects.create(
                text=f'Test memory {i}',
                conversation_id='test-conv-1'
            )
    
    def test_list_memories(self):
        """Test listing memories for a conversation"""
        response = self.client.get('/api/mcp/listMemories?conversation_id=test-conv-1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertEqual(len(response.data['data']['memories']), 5)
        self.assertEqual(response.data['data']['total'], 5)


class ChatTestCase(TestCase):
    """Test chat endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_chat_basic(self):
        """Test basic chat functionality"""
        data = {
            'conversation_id': 'test-conv-1',
            'message': 'Hello, world!'
        }
        response = self.client.post('/api/chat', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertIn('reply', response.data['data'])
    
    def test_chat_with_remember(self):
        """Test chat with memory storage"""
        data = {
            'conversation_id': 'test-conv-1',
            'message': 'Remember this',
            'remember': True
        }
        response = self.client.post('/api/chat', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['data']['memory_injected'])
        
        # Verify memories were created
        memories = Memory.objects.filter(conversation_id='test-conv-1')
        self.assertGreater(memories.count(), 0)


class AuthTestCase(TestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register', self.test_user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['ok'])
        self.assertIn('token', response.data['data'])
        self.assertIn('refresh', response.data['data'])
    
    def test_login_user(self):
        """Test user login"""
        # Create user first
        User.objects.create_user(**self.test_user_data)
        
        # Login
        login_data = {
            'username': self.test_user_data['username'],
            'password': self.test_user_data['password']
        }
        response = self.client.post('/api/auth/login', login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertIn('token', response.data['data'])
    
    def test_get_profile(self):
        """Test getting user profile"""
        # Create and authenticate user
        user = User.objects.create_user(**self.test_user_data)
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/api/auth/profile')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertEqual(response.data['data']['username'], self.test_user_data['username'])


class ConversationTestCase(TestCase):
    """Test conversation endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_conversation(self):
        """Test creating a conversation"""
        data = {'title': 'Test Conversation'}
        response = self.client.post('/api/conversations/create', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['ok'])
        self.assertEqual(response.data['data']['title'], 'Test Conversation')
    
    def test_list_conversations(self):
        """Test listing conversations"""
        # Create test conversations
        Conversation.objects.create(user=self.user, title='Conv 1')
        Conversation.objects.create(user=self.user, title='Conv 2')
        
        response = self.client.get('/api/conversations')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertEqual(response.data['data']['total'], 2)
    
    def test_delete_conversation(self):
        """Test deleting a conversation"""
        conv = Conversation.objects.create(user=self.user, title='To Delete')
        
        response = self.client.delete(f'/api/conversations/{conv.id}/delete')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertFalse(Conversation.objects.filter(id=conv.id).exists())


class MemoryManagementTestCase(TestCase):
    """Test memory management endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_delete_memory(self):
        """Test deleting a specific memory"""
        memory = Memory.objects.create(
            text='Test memory to delete',
            conversation_id='test-conv'
        )
        
        response = self.client.delete(f'/api/mcp/memory/{memory.id}/delete')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertFalse(Memory.objects.filter(id=memory.id).exists())
    
    def test_clear_conversation_memories(self):
        """Test clearing all memories for a conversation"""
        # Create multiple memories
        for i in range(3):
            Memory.objects.create(
                text=f'Memory {i}',
                conversation_id='test-conv'
            )
        
        response = self.client.delete('/api/mcp/conversation/test-conv/clear')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertEqual(response.data['data']['count'], 3)


class SpecHookTestCase(TestCase):
    """Test spec hook endpoint"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_spec_hook_updates_file(self):
        """Test that spec hook appends to spec.md"""
        data = {
            'type': 'test-endpoint',
            'path': '/api/test',
            'method': 'GET',
            'description': 'Test endpoint for unit tests'
        }
        response = self.client.post('/api/hooks/spec-update', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ok'])
        self.assertTrue(response.data['data']['updated'])
