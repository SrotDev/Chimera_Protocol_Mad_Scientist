"""
Fix model IDs in existing conversations
Converts "model-gemini-20-flash" to "model-gemini-2.0-flash"
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chimera.settings')
django.setup()

from api.models import Conversation

# Mapping of old format to new format
MODEL_ID_FIXES = {
    'model-gemini-20-flash': 'model-gemini-2.0-flash',
    'model-gemini-15-flash': 'model-gemini-1.5-flash',
    'model-gemini-15-pro': 'model-gemini-1.5-pro',
    'model-gpt4o': 'model-gpt-4o',
    'model-gpt4': 'model-gpt-4',
    'model-gpt4-turbo': 'model-gpt-4-turbo',
    'model-gpt35-turbo': 'model-gpt-3.5-turbo',
    'model-claude3-opus': 'model-claude-3-opus',
    'model-claude3-sonnet': 'model-claude-3-sonnet',
    'model-claude3-haiku': 'model-claude-3-haiku',
    'model-claude35-sonnet': 'model-claude-3.5-sonnet',
}

def fix_model_ids():
    """Fix model IDs in all conversations"""
    updated_count = 0
    
    for old_id, new_id in MODEL_ID_FIXES.items():
        conversations = Conversation.objects.filter(model_id=old_id)
        count = conversations.count()
        
        if count > 0:
            print(f"Updating {count} conversations from '{old_id}' to '{new_id}'")
            conversations.update(model_id=new_id)
            updated_count += count
    
    print(f"\n✅ Updated {updated_count} conversations total")
    
    # Show current model IDs
    print("\nCurrent model IDs in database:")
    for conv in Conversation.objects.all():
        print(f"  - {conv.id}: {conv.model_id}")

if __name__ == '__main__':
    fix_model_ids()
