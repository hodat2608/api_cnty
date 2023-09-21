from rest_framework.response import Response
from .models import Note 
from .serializers import NoteSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserAccount
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .permissions import ModifyNotePermisson
@api_view(['GET'])
def getRouter(request):
    return Response('I dont give up, i just take a rest, after that i keep going')
    
class Note_List(APIView):
    def get(self,request,format=None):
        note = Note.objects.all() 
        serializer = NoteSerializer(note,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        data = request.data
        data['user'] = request.user.id
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Action(APIView):

    def get_object(self,pk):
        try: 
            return  Note.objects.get(pk=pk) 
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk,format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk, format=None):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ownnoteuser(viewsets.ViewSet):
    permission_classes =[IsAuthenticated]
    authentication_classes = [BasicAuthentication,SessionAuthentication,TokenAuthentication] 
    def get_user(self,request):
        try:
            return UserAccount.objects.get(id=request.user.id)
        except UserAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=False, methods=['get'])
    def get_all_note(self,request):
        notes = Note.objects.filter(user_id=request.user.id) 
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def add_note(self,request,format=None):
        data = request.data
        serializer = NoteSerializer(data=data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])  
    def modify_note(self, request, pk=None, format=None):
        note = Note.objects.get(pk=pk)
        data = request.data
        data['user'] = request.user.id
        serializer = NoteSerializer(note, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    @action(detail=True, methods=['delete'])  
    def delete_note(self, request, pk=None, format=None):
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get','delete'])  
    def detail_note(self, request, pk=None, format=None):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note)
        if request.method == 'GET':
            return Response(serializer.data)   
        if request.method == 'DELETE':
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
