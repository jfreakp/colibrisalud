import os
import sys
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.insert(0, '/var/task')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colibrisalud.settings')

# Setup Django
django.setup()

# Get the WSGI application
app = get_wsgi_application()

# Vercel serverless handler
def handler(request):
    return app(request)
