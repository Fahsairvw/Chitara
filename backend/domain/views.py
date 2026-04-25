import os
import logging
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Library, Song
from .models.choices import SongStatus, Genre, Occasion
from .serializers import UserSerializer, LibrarySerializer, SongSerializer
from .services import MusicService

logger = logging.getLogger(__name__)


# CHOICES
@api_view(["GET"])
def choices(request):
    """Return Genre and Occasion choices defined in the model."""
    return Response({
        "genres": [{"value": v, "label": l} for v, l in Genre.choices],
        "occasions": [{"value": v, "label": l} for v, l in Occasion.choices],
    })


# USER
@api_view(["GET", "POST"])
def users(request):

    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# LIBRARY
@api_view(["GET", "POST"])
def libraries(request):

    if request.method == "GET":
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = LibrarySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


# SONG
@api_view(["GET", "POST", "PUT"])
def songs(request):

    if request.method == "GET":
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        try:
            user_id = request.data.get("user")
            library_id = request.data.get("library")
            
            user = User.objects.get(pk=user_id)
            library = Library.objects.get(pk=library_id)
            
            service = MusicService()
            song, result = service.generate_song(user, library, request.data)
            
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except (User.DoesNotExist, Library.DoesNotExist) as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    if request.method == "PUT":
        song_id = request.data.get("id")
        if not song_id:
            return Response({"error": "Song ID is required in request body"})
       
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"})
       
        serializer = SongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       
        return Response(serializer.errors)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def song_detail(request, pk):

    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"})

    if request.method == "GET":
        serializer = SongSerializer(song)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = SongSerializer(song, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    if request.method == "PATCH":
        serializer = SongSerializer(song, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    if request.method == "DELETE":
        song.delete()
        return Response({"message": "Song deleted"})


@api_view(["POST"])
def create_song(request):

    user = User.objects.get(id=request.data["user"])
    library = Library.objects.get(id=request.data["library"])

    service = MusicService()

    song, result = service.generate_song(user, library, request.data)

    return Response({
        "song_id": song.id,
        "status": result["status"],
        "taskId": result.get("taskId"),
        "url": result.get("url")
    })


@api_view(["GET"])
def check_song(request, task_id):

    try:
        song = Song.objects.get(task_id=task_id)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"})

    url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={task_id}"

    headers = {
        "Authorization": f"Bearer {os.getenv('SUNO_API_KEY')}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Failed to fetch from Suno: {str(e)}"}, status=500)

    api_status = data.get("data", {}).get("status")

    # Always update the song status from Suno API
    if api_status == "SUCCESS":
        suno_list = data.get("data", {}).get("response", {}).get("sunoData", [])
        
        if len(suno_list) > 0:
            audio_url = suno_list[0].get("audioUrl")
            song.link = audio_url
            song.status = SongStatus.SUCCEEDED
            song.save()
    
    elif api_status == "PENDING":
        song.status = SongStatus.PENDING
        song.save()
    
    elif api_status == "FAILED":
        song.status = SongStatus.FAILED
        song.save()

    return Response({
        "song_id": song.id,
        "status": song.status,
        "link": song.link,
        "api_response": data
    })


# GOOGLE OAUTH REDIRECT - Start OAuth flow
@api_view(["GET"])
def google_oauth_start(request):
    """
    Redirect to Google for authentication
    """
    CLIENT_ID = os.getenv('CLIENT_ID')
    REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback/')
    
    # Build Google OAuth URL - simple format
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    
    return Response({"auth_url": auth_url})


# GOOGLE OAUTH CALLBACK - Handle Google redirect
@api_view(["GET"])
def google_oauth_callback(request):
    """
    Handle Google OAuth callback - exchange code for token
    """
    import requests
    
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return Response({"error": f"Google auth error: {error}"}, status=400)
    
    if not code:
        return Response({"error": "No authorization code received"}, status=400)
    
    try:
        CLIENT_ID = os.getenv('CLIENT_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback/')
        
        # Exchange code for token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        token_response_data = token_response.json()
        
        id_token = token_response_data.get('id_token')
                
        # Get user info from Google
        userinfo_url = 'https://openidconnect.googleapis.com/v1/userinfo'
        headers = {'Authorization': f"Bearer {token_response_data.get('access_token')}"}
        
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
        
        logger.debug(f"User info: {userinfo}")
        
        email = userinfo.get('email')
        first_name = userinfo.get('given_name', '').strip() or 'User'
        last_name = userinfo.get('family_name', '').strip() or 'Account'
        
        if not email:
            return Response({"error": "Email not found in Google account"}, status=400)
        
        # Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'firstName': first_name,
                'lastName': last_name,
                'role': 'User'
            }
        )
        
        logger.info(f"User {'created' if created else 'found'}: {user.id}")
        
        # Create or get library
        library, _ = Library.objects.get_or_create(
            user=user,
            defaults={'name': f"{first_name}'s Music Library"}
        )
        
        # Generate auth token
        import time
        auth_token = f"token_{user.id}_{int(time.time())}"
        
        # Redirect to frontend with token
        FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        frontend_redirect = f"{FRONTEND_URL}/?auth_token={auth_token}&user={user.id}"
        
        logger.info(f"User {user.id} authenticated, redirecting to frontend: {frontend_redirect}")
        
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(frontend_redirect)
        
    except Exception as e:
        logger.error(f"Error in google_oauth_callback: {str(e)}", exc_info=True)
        return Response({
            "error": f"Google authentication failed: {str(e)}"
        }, status=500)


# GOOGLE OAUTH TOKEN - Verify token (fallback)
@api_view(["POST"])
def google_auth(request):
    """
    Handle Google OAuth ID token verification (fallback for direct token)
    """
    id_token_str = request.data.get('id_token')    
    if not id_token_str:
        return Response({"error": "No ID token provided"}, status=400)
    
    try:
        import json
        import base64
        
        # Decode JWT payload (basic - not cryptographically verified)
        parts = id_token_str.split('.')
        logger.debug(f"Token parts: {len(parts)}")
        
        if len(parts) < 2:
            raise ValueError(f"Invalid token format - expected 3 parts, got {len(parts)}")
        
        # Decode payload
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        
        try:
            idinfo = json.loads(base64.urlsafe_b64decode(payload))
            logger.debug(f"Decoded token info: {idinfo}")
        except Exception as e:
            logger.debug(f"Failed to decode token: {str(e)}")
            raise ValueError(f"Invalid token payload: {str(e)}")
        
        # Extract user information
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '').strip() or 'User'
        last_name = idinfo.get('family_name', '').strip() or 'Account'
        
        logger.debug(f"Extracted email={email}, first_name={first_name}, last_name={last_name}")
        
        if not email:
            return Response({"error": "Email not found in token"}, status=400)
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'firstName': first_name,
                'lastName': last_name,
                'role': 'User'
            }
        )
        
        logger.info(f"User {'created' if created else 'found'}: {user.id}")
        
        # Create or get user's library
        library, _ = Library.objects.get_or_create(
            user=user,
            defaults={'name': f"{first_name}'s Music Library"}
        )
        
        # Generate simple auth token
        import time
        auth_token = f"token_{user.id}_{int(time.time())}"
        
        # Serialize user
        serializer = UserSerializer(user)
        
        logger.info(f"Login successful for user {user.id}")
        
        return Response({
            "token": auth_token,
            "user": serializer.data,
            "message": "Google login successful"
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in google_auth: {str(e)}", exc_info=True)
        return Response({
            "error": f"Authentication failed: {str(e)}"
        }, status=500)
