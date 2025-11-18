from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.conf import settings
import json
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import cloudinary.uploader

from .utils import get_gemini_response # Import the new utility function

