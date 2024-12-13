import os
import sys

# Set the settings module to the project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_analytics.settings')

# Import Django and the necessary modules
import django
django.setup()

from django.contrib.sessions.models import Session
import sys

# List all session records and their keys
session_records = Session.objects.all()  

# Get the latest session object's key
key = Session.objects.latest('session_data').session_key
session_obj = Session.objects.get(session_key = key)

encoded_data = session_obj.session_data

# Decode the session data
session_data = session_obj.get_decoded()

session_bytes = sys.getsizeof(encoded_data)

print(f'Session size in bytes: {session_bytes}')

# session_obj.delete()