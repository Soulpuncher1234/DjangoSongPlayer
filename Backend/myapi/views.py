from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import FileResponse

from .models import Song
from .serializers import SongSerializer

import base64
import pathlib
import os

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['POST', 'GET'])
def saveSong(request):

    if request.method == 'POST':
        serializer = SongSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    elif request.method == 'GET':
        Songs = Song.objects.all()
        serializer = SongSerializer(Songs, many=True)
        return Response(serializer.data)
    
    

@api_view(['GET', 'DELETE'])
def getSong(request, id):

    if request.method == 'GET':
        # Find the song object with the correspoding id
        serialzer = SongSerializer(Song.objects.get(pk=id))

        #Find the file path of the audio file and encode it to base64 as image data
        # print(Song.objects.get(pk=id).audio)

        # with open(Song.objects.get(pk=id).audio, "rb") as file:
        #     file_data = f.read()
        return Response({"SongDetails":serialzer.data})
    
    elif request.method == 'DELETE':
        audio_path = "media/" + str(Song.objects.get(pk=id).audio)
        image_path = "media/" + str(Song.objects.get(pk=id).image)

        if os.path.isfile(audio_path):
            os.remove(audio_path)

        if os.path.isfile(image_path):
            os.remove(image_path)

        Song.objects.get(pk=id).delete()


        return Response({"message": "Successful delete"})

@api_view(['GET'])
def getImageFile(request, id):
    if request.method == 'GET':
        # Get the file path
        #img = open('media/soundFiles/hd/algo.jpg','rb')
        #return FileResponse(img, as_attachment=True)

        file_path = "media/" + str(Song.objects.get(pk=id).image)
        print(file_path)

        with open(file_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        return Response({"b64":image_data, "dataType":pathlib.Path(file_path).suffix[1:]})

@api_view(['GET'])
def getAudioFile(request, id):
    if request.method == 'GET':
        file_path = "media/" + str(Song.objects.get(pk=id).audio)

        with open(file_path, 'rb') as f:
            song_data = base64.b64encode(f.read()).decode('utf-8')
        return Response({"b64": song_data, "dataType": pathlib.Path(file_path).suffix[1:]})

@api_view(['GET'])
def getAllSongs(request):
    if request.method == 'GET':
        Songs = Song.objects.all()
        serializer = SongSerializer(Songs, many=True)
        return Response(serializer.data)