from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Note 
from .serializers import NoteSerializer
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def getRouter(request):
    return Response('I dont give up, i just take a rest, after that i keep going')

@api_view(['GET','POST'])
def getNote(request):
    #all note
    if request.method == 'GET':
        note = Note.objects.all() 
        serializer = NoteSerializer(note,many=True)
        return Response(serializer.data)
    #add another note 
    elif request.method =='POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def detail_note(request,id): 
    try : 
        note = Note.objects.get(pk=id) 
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #details note with id
    if request.method == 'GET':
        serializer = NoteSerializer(note,many=False)
        return Response(serializer.data)
    #update note
    elif request.method == 'PUT':
        serializer = NoteSerializer(instance=note,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    

    