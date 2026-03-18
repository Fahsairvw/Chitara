from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Library, Song
from .serializers import UserSerializer, LibrarySerializer, SongSerializer

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
@api_view(["GET", "POST"])
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
