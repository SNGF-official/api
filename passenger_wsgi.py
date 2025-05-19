import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))  # noqa: PTH120

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))  # noqa: PTH120, PTH118

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


application = get_wsgi_application()
