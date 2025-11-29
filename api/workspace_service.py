"""
Workspace Statistics Calculation Service

This module provides functions for calculating workspace statistics
including memory counts, conversation counts, system load, and last activity.
"""
from django.utils import timezone
from django.db.models import Q, Max, Count
from datetime import timedelta


def calculate_workspace_stats(workspace):
    """
    Calculate comprehensive statistics for a workspace.
    
    Args:
        workspace: Workspace model instance
        
    Returns:
        dict: Statistics including:
            - totalMemories: Count of all memories in workspace
            - totalEmbeddings: Count of memories with non-null embedding
            - totalConversations: Count of all conversations in workspace
            - systemLoad: Calculated load percentage (0-100)
            - lastActivity: Most recent timestamp across all entities
    
    Requirements: 2.6, 8.1, 8.4
    """
    # Calculate totalMemories (count of workspace memories)
    total_memories = workspace.memories.count()
    
    # Calculate totalEmbeddings (count of memories with non-null embedding)
    total_embeddings = workspace.memories.filter(embedding__isnull=False).count()
    
    # Calculate totalConversations (count of workspace conversations)
    total_conversations = workspace.conversations.count()
    
    # Calculate systemLoad using formula: (active_conversations * 10 + messages_last_hour) capped at 100
    system_load = _calculate_system_load(workspace)
    
    # Calculate lastActivity (most recent timestamp across all entities)
    last_activity = _calculate_last_activity(workspace)
    
    return {
        'totalMemories': total_memories,
        'totalEmbeddings': total_embeddings,
        'totalConversations': total_conversations,
        'systemLoad': system_load,
        'lastActivity': last_activity
    }


def _calculate_system_load(workspace):
    """
    Calculate system load using the formula:
    (active_conversations * 10 + messages_last_hour) capped at 100
    
    Args:
        workspace: Workspace model instance
        
    Returns:
        int: System load percentage (0-100)
        
    Requirements: 8.4
    """
    # Count active conversations
    active_conversations = workspace.conversations.filter(status='active').count()
    
    # Count messages in the last hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    messages_last_hour = 0
    
    # Get all conversations and count their messages from last hour
    for conversation in workspace.conversations.all():
        messages_last_hour += conversation.messages.filter(
            timestamp__gte=one_hour_ago
        ).count()
    
    # Apply formula: (active_conversations * 10 + messages_last_hour) capped at 100
    system_load = (active_conversations * 10) + messages_last_hour
      
    system_load = min(100, system_load)
    
    return system_load


def record_load_snapshot(workspace):
    """
    Record current system load as a snapshot for historical tracking.
    Called when significant activity occurs (message sent, conversation created, etc.)
    
    Args:
        workspace: Workspace model instance
    """
    from .models import SystemLoadSnapshot
    
    # Calculate current load
    system_load = _calculate_system_load(workspace)
    
    # Create snapshot
    SystemLoadSnapshot.objects.create(
        workspace=workspace,
        value=system_load
    )
    
    # Clean up old snapshots (keep last 24 hours worth, ~288 at 5-min intervals)
    from django.utils import timezone
    cutoff = timezone.now() - timedelta(hours=24)
    workspace.load_snapshots.filter(timestamp__lt=cutoff).delete()


def get_neural_load_history(workspace, points=24):
    """
    Get historical load data for the neural load monitor.
    Returns actual stored snapshots, filling gaps with interpolation.
    
    Args:
        workspace: Workspace model instance
        points: Number of data points to return (default 24)
        
    Returns:
        list: Array of timestamp-value pairs
    """
    from .models import SystemLoadSnapshot
    from django.utils import timezone
    
    now = timezone.now()
    interval_minutes = 5
    
    # Get snapshots from last 2 hours (24 points * 5 min = 120 min)
    cutoff = now - timedelta(minutes=points * interval_minutes)
    snapshots = list(workspace.load_snapshots.filter(
        timestamp__gte=cutoff
    ).order_by('timestamp'))
    
    # If no snapshots, return current load for all points
    if not snapshots:
        current_load = _calculate_system_load(workspace)
        return [
            {
                'timestamp': now - timedelta(minutes=(points - 1 - i) * interval_minutes),
                'value': current_load
            }
            for i in range(points)
        ]
    
    # Build time series with actual data
    result = []
    snapshot_idx = 0
    
    for i in range(points):
        target_time = now - timedelta(minutes=(points - 1 - i) * interval_minutes)
        
        # Find closest snapshot to this time point
        best_snapshot = None
        best_diff = timedelta(minutes=interval_minutes)  # Max acceptable diff
        
        for snap in snapshots:
            diff = abs(snap.timestamp - target_time)
            if diff < best_diff:
                best_diff = diff
                best_snapshot = snap
        
        if best_snapshot:
            result.append({
                'timestamp': target_time,
                'value': best_snapshot.value
            })
        else:
            # No snapshot near this time, use interpolation or last known value
            if result:
                result.append({
                    'timestamp': target_time,
                    'value': result[-1]['value']
                })
            else:
                result.append({
                    'timestamp': target_time,
                    'value': _calculate_system_load(workspace)
                })
    
    return result


def _calculate_last_activity(workspace):
    """
    Calculate the most recent timestamp across all workspace entities.
    
    Checks:
    - Workspace updated_at
    - Most recent memory updated_at
    - Most recent conversation updated_at
    - Most recent message timestamp
    - Most recent activity timestamp
    
    Args:
        workspace: Workspace model instance
        
    Returns:
        datetime: Most recent timestamp
        
    Requirements: 2.6, 8.1
    """
    # Start with workspace updated_at
    last_activity = workspace.updated_at
    
    # Check most recent memory
    latest_memory = workspace.memories.order_by('-updated_at').first()
    if latest_memory and latest_memory.updated_at > last_activity:
        last_activity = latest_memory.updated_at
    
    # Check most recent conversation
    latest_conversation = workspace.conversations.order_by('-updated_at').first()
    if latest_conversation and latest_conversation.updated_at > last_activity:
        last_activity = latest_conversation.updated_at
    
    # Check most recent message across all conversations
    # Use aggregate to get max timestamp efficiently
    from .models import ChatMessage
    latest_message_time = ChatMessage.objects.filter(
        conversation__workspace=workspace
    ).aggregate(Max('timestamp'))['timestamp__max']
    
    if latest_message_time and latest_message_time > last_activity:
        last_activity = latest_message_time
    
    # Check most recent activity
    latest_activity = workspace.activities.order_by('-timestamp').first()
    if latest_activity and latest_activity.timestamp > last_activity:
        last_activity = latest_activity.timestamp
    
    return last_activity
