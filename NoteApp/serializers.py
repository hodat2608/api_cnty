from rest_framework.serializers import ModelSerializer 
from .models import Note
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note 
        fields = '__all__'