"""
Django admin configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Memory, Conversation, ChatMessage, Workspace, TeamMember, 
    Integration, WorkspaceInvitation, ConversationMemory, Activity, SystemLoadSnapshot
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'name']
    readonly_fields = ['id', 'date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'avatar')}),
        ('Memory Settings', {'fields': ('auto_store', 'retention_period')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2'),
        }),
    )


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'workspace', 'created_at']
    list_filter = ['created_at', 'workspace']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'workspace', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'status']
    search_fields = ['title', 'workspace__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'role', 'content_preview', 'timestamp']
    list_filter = ['role', 'timestamp']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'workspace', 'role', 'status', 'joined_at']
    list_filter = ['role', 'status', 'joined_at']
    search_fields = ['user__username', 'workspace__name']
    readonly_fields = ['id', 'joined_at']


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'provider', 'status', 'last_tested']
    list_filter = ['provider', 'status', 'created_at']
    search_fields = ['user__username', 'provider']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(WorkspaceInvitation)
class WorkspaceInvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'workspace', 'inviter', 'invitee', 'status', 'created_at', 'responded_at']
    list_filter = ['status', 'created_at']
    search_fields = ['workspace__name', 'inviter__username', 'invitee__username', 'invitee__email']
    readonly_fields = ['id', 'created_at']


@admin.register(ConversationMemory)
class ConversationMemoryAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'memory', 'is_active', 'injected_at']
    list_filter = ['is_active', 'injected_at']
    search_fields = ['conversation__title', 'memory__title']
    readonly_fields = ['injected_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'workspace', 'type', 'description_preview', 'timestamp']
    list_filter = ['type', 'timestamp', 'workspace']
    search_fields = ['description', 'workspace__name']
    readonly_fields = ['id', 'timestamp']
    
    def description_preview(self, obj):
        return obj.description[:80] + '...' if len(obj.description) > 80 else obj.description
    description_preview.short_description = 'Description'


@admin.register(SystemLoadSnapshot)
class SystemLoadSnapshotAdmin(admin.ModelAdmin):
    list_display = ['id', 'workspace', 'value', 'timestamp']
    list_filter = ['timestamp', 'workspace']
    search_fields = ['workspace__name']
    readonly_fields = ['id', 'timestamp']
