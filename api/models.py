"""
Database models for Chimera Protocol API
"""
from django.db import models
from django.contrib.auth.models import User
import uuid


class Conversation(models.Model):
    """
    Represents a conversation session between user and AI
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['user', '-updated_at']),
        ]

    def __str__(self):
        return f"Conversation {self.id} - {self.title or 'Untitled'}"


class Memory(models.Model):
    """
    Stores memory fragments with vector embeddings for semantic search
    """
    text = models.TextField(help_text="The memory content")
    tags = models.JSONField(default=list, blank=True, help_text="Tags for categorization")
    conversation_id = models.CharField(
        max_length=128, 
        db_index=True,
        help_text="Associated conversation ID"
    )
    embedding = models.BinaryField(
        null=True, 
        blank=True,
        help_text="Vector embedding for similarity search"
    )
    metadata = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Additional metadata"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['conversation_id', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        preview = self.text[:50] + '...' if len(self.text) > 50 else self.text
        return f"Memory {self.id}: {preview}"


class ChatMessage(models.Model):
    """
    Stores individual chat messages
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
