from rest_framework.serializers import ModelSerializer 
from .models import Note
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note 
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        note = Note.objects.create(user=user, **validated_data)
        return note