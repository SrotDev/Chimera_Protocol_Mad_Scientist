"""
Data Cleanup Service for Memory Retention
Handles automatic deletion of user workspaces based on retention period settings.
"""
from django.utils import timezone
from datetime import timedelta
from .models import User, Workspace


def get_retention_days(retention_period: str) -> int | None:
    """Convert retention period string to number of days. Returns None for indefinite."""
    mapping = {
        '7-days': 7,
        '30-days': 30,
        '90-days': 90,
        'indefinite-84': 84,
        'indefinite-forever': None,
    }
    return mapping.get(retention_period)


def get_user_cleanup_info(user: User) -> dict:
    """
    Get cleanup information for a user including next cleanup date and time remaining.
    Returns dict with cleanup_date, days_remaining, hours_remaining, is_indefinite.
    """
    retention_days = get_retention_days(user.retention_period)
    
    if retention_days is None:
        return {
            'cleanup_date': None,
            'days_remaining': None,
            'hours_remaining': None,
            'minutes_remaining': None,
            'is_indefinite': True,
            'retention_period': user.retention_period,
        }
    
    # Calculate cleanup date based on user's account creation or last cleanup
    # Using date_joined as the reference point
    cleanup_date = user.date_joined + timedelta(days=retention_days)
    
    # If cleanup date has passed, calculate next cycle
    now = timezone.now()
    while cleanup_date <= now:
        cleanup_date += timedelta(days=retention_days)
    
    time_remaining = cleanup_date - now
    total_seconds = time_remaining.total_seconds()
    
    days = int(total_seconds // 86400)
    hours = int((total_seconds % 86400) // 3600)
    minutes = int((total_seconds % 3600) // 60)
    
    return {
        'cleanup_date': cleanup_date.isoformat(),
        'days_remaining': days,
        'hours_remaining': hours,
        'minutes_remaining': minutes,
        'total_seconds_remaining': int(total_seconds),
        'is_indefinite': False,
        'retention_period': user.retention_period,
    }


def cleanup_user_data(user: User) -> dict:
    """
    Delete all workspaces owned by the user (cascades to conversations, memories, etc.)
    Returns summary of deleted items.
    """
    owned_workspaces = Workspace.objects.filter(owner=user)
    workspace_count = owned_workspaces.count()
    
    # Get counts before deletion for summary
    from .models import Conversation, Memory, ChatMessage
    
    conversation_count = Conversation.objects.filter(workspace__owner=user).count()
    memory_count = Memory.objects.filter(workspace__owner=user).count()
    message_count = ChatMessage.objects.filter(conversation__workspace__owner=user).count()
    
    # Delete all owned workspaces (cascades to related data)
    owned_workspaces.delete()
    
    return {
        'workspaces_deleted': workspace_count,
        'conversations_deleted': conversation_count,
        'memories_deleted': memory_count,
        'messages_deleted': message_count,
        'cleanup_time': timezone.now().isoformat(),
    }


def run_scheduled_cleanup():
    """
    Run cleanup for all users whose retention period has expired.
    This should be called by a scheduled task (e.g., celery beat, cron job).
    """
    now = timezone.now()
    cleanup_results = []
    
    for user in User.objects.exclude(retention_period='indefinite-forever'):
        retention_days = get_retention_days(user.retention_period)
        if retention_days is None:
            continue
        
        cleanup_date = user.date_joined + timedelta(days=retention_days)
        
        # Check if cleanup is due
        while cleanup_date <= now:
            # Perform cleanup
            result = cleanup_user_data(user)
            result['user_id'] = str(user.id)
            result['user_email'] = user.email
            cleanup_results.append(result)
            
            # Move to next cycle
            cleanup_date += timedelta(days=retention_days)
    
    return cleanup_results
