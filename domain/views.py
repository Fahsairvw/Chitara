import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Library, Song
from .serializers import UserSerializer, LibrarySerializer, SongSerializer
from .services import MusicService


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
        serializer = SongSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

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
            song.status = "SUCCEEDED"
            song.save()
    
    elif api_status == "PENDING":
        song.status = "GENERATING"
        song.save()
    
    elif api_status == "FAILED":
        song.status = "FAILED"
        song.save()

    return Response({
        "song_id": song.id,
        "status": song.status,
        "link": song.link,
        "api_response": data
    })
