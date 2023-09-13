from rest_framework.response import Response
from .models import Note 
from .serializers import NoteSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def getRouter(request):
    return Response('I dont give up, i just take a rest, after that i keep going')
    
class Note_List(APIView):
    # authentication_classes = [BasicAuthentication,SessionAuthentication]
    # permission_classes =[IsAuthenticated] 
               
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
        except:
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
