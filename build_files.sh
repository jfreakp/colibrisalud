#!/bin/bash
echo "Building Django project..."
python -m pip install -r requirements.txt --quiet
python manage.py collectstatic --noinput 2>/dev/null || true
echo "Build completed!"
