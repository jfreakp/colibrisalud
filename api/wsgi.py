import os
import sys
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, '/var/task')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'colibrisalud.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
