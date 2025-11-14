from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .serializers import DocumentCommentSerializer
from django.conf import settings
import google.generativeai as genai
import json
from django.http import FileResponse, HttpResponse
import markdown
from xhtml2pdf import pisa
from io import BytesIO
from .mongo_client import get_all_conversations, get_conversation_by_id, save_conversation, update_conversation, delete_conversation, get_document_version_content
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.crypto import get_random_string
import os
import cloudinary.uploader
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
import asyncio
from django.db import connection
import threading
import time

# Create a thread pool executor for handling long-running tasks
executor = ThreadPoolExecutor(max_workers=8)


@api_view(['POST'])
def generate_share_link(request):
    """
    Generates a shareable link for a document, even if it's not saved.
    """
    document_content = request.data.get('document_content')
    title = request.data.get('title', 'Shared Document')
    
    if not document_content:
        return Response({'error': 'Document content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create a temporary conversation with the document
        conversation_id = save_conversation(
            title=title,
            messages=[],
            initial_document_content=document_content,
            uploaded_by=(request.user.username if request.user.is_authenticated else 'anonymous'),
            notes='Shared document'
        )
        
        share_url = f"/shared/{conversation_id}"
        return Response({'share_url': share_url}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Error generating share link: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def document_comments(request, document_id):
    if request.method == 'GET':
        try:
            comments = DocumentComment.objects.filter(document_id=document_id).values(
                'id', 'user', 'content', 'position', 'created_at', 'parent_comment_id'
            )
            return Response(list(comments))
        except Exception as e:
            print(f"Error getting comments: {e}")  # Debug print
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            data = request.data
            content = data.get('content')
            if not content:
                return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

            print(f"Creating comment with data: {data}")  # Debug print

            comment = DocumentComment.objects.create(
                document_id=document_id,
                user=request.user.username if request.user.is_authenticated else 'anonymous',
                content=content,
                position=data.get('position'),
                parent_comment_id=data.get('parent_comment_id')
            )

            print(f"Comment created successfully: {comment}")  # Debug print

            return Response({
                'id': comment.id,
                'user': comment.user,
                'content': comment.content,
                'position': comment.position,
                'created_at': comment.created_at,
                'parent_comment_id': comment.parent_comment_id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error creating comment: {e}")  # Debug print
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Added by maharshi
@api_view(['POST'])
@parser_classes([JSONParser])
def create_document_comment(request):
    """
    Creates a new comment for a document.
    """
    try:
        data = request.data
        document_id = data.get('document_id')
        content = data.get('content')

        if not document_id or not content:
            return Response({'error': 'Document ID and content are required'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Creating comment with data: {data}")  # Debug print

        comment = DocumentComment.objects.create(
            document_id=document_id,
            user=request.user.username if request.user.is_authenticated else 'anonymous',
            content=content,
            position=data.get('position'),
            parent_comment_id=data.get('parent_comment_id')
        )

        print(f"Comment created: {comment}")  # Debug print

        return Response({
            'id': comment.id,
            'user': comment.user,
            'content': comment.content,
            'position': comment.position,
            'created_at': comment.created_at,
            'parent_comment_id': comment.parent_comment_id
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(f"Error creating comment: {e}")  # Debug print
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@with_timeout(60)  # Increased timeout for conversation operations
def conversation_list(request):
    """
    List all conversations or create a new one.
    """
    try:
        reset_db_connection()
        
        if request.method == 'GET':
            conversations = get_all_conversations()
            return Response(conversations)

        elif request.method == 'POST':
            title = request.data.get('title')
            messages = request.data.get('messages')
            initial_document_content = request.data.get('initial_document_content')
            notes = request.data.get('notes', 'Initial Version')

            if not title or messages is None:  # Allow empty list but not None
                return Response(
                    {'error': 'Title is required and messages must be a list'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add retries for MongoDB operations
            max_retries = 3
            retry_delay = 1  # seconds
            
            for attempt in range(max_retries):
                try:
                    conversation_id = save_conversation(
                        title, 
                        messages, 
                        initial_document_content, 
                        uploaded_by=(request.user.username if request.user.is_authenticated else 'anonymous'), 
                        notes=notes
                    )
                    
                    if conversation_id:
                        return Response({
                            'id': conversation_id,
                            'message': 'Document saved successfully'
                        }, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        raise
                    time.sleep(retry_delay)
                    continue

            return Response(
                {'error': 'Failed to save conversation after multiple attempts'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        print(f"Error in conversation_list: {str(e)}")
        return Response(
            {'error': f'An unexpected error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'PUT', 'DELETE'])
@with_timeout(60)  # Increased timeout for conversation operations
def conversation_detail(request, pk):
    """
    Retrieve, update or delete a single conversation.
    """
    try:
        reset_db_connection()
        
        if request.method == 'GET':
            conversation = get_conversation_by_id(pk)
            if conversation:
                return Response(conversation)
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        elif request.method == 'PUT':
            title = request.data.get('title')
            messages = request.data.get('messages')
            new_document_content = request.data.get('new_document_content')
            notes = request.data.get('notes', f'Version update via AI editor')

            if not title or messages is None:  # Allow empty list but not None
                return Response(
                    {'error': 'Title is required and messages must be a list'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add retries for MongoDB operations
            max_retries = 3
            retry_delay = 1  # seconds
            
            for attempt in range(max_retries):
                try:
                    success = update_conversation(
                        pk, 
                        title, 
                        messages, 
                        new_document_content, 
                        uploaded_by=(request.user.username if request.user.is_authenticated else 'anonymous'), 
                        notes=notes
                    )
                    
                    if success:
                        return Response({
                            'status': 'success',
                            'message': 'Document updated successfully'
                        }, status=status.HTTP_200_OK)
                        
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        raise
                    time.sleep(retry_delay)
                    continue

            return Response(
                {'error': 'Failed to update conversation after multiple attempts'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        elif request.method == 'DELETE':
            success = delete_conversation(pk)
            if success:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error': 'Failed to delete conversation'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        print(f"Error in conversation_detail: {str(e)}")
        return Response(
            {'error': f'An unexpected error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
