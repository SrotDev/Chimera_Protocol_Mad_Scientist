"""
Fix invalid integrations by deleting them so they can be re-added
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chimera.settings')
django.setup()

from api.models import Integration

def fix_integrations():
    """Delete all integrations so they can be re-added with correct encryption"""
    integrations = Integration.objects.all()
    count = integrations.count()
    
    if count > 0:
        print(f"Found {count} integrations:")
        for integration in integrations:
            print(f"  - {integration.provider} (status: {integration.status})")
        
        print(f"\nDeleting all {count} integrations...")
        integrations.delete()
        print("✅ All integrations deleted")
        print("\nPlease re-add your API integrations in the frontend:")
        print("1. Go to Settings > Integrations")
        print("2. Add your Google API key")
        print("3. Test the connection")
    else:
        print("No integrations found")

if __name__ == '__main__':
    fix_integrations()
