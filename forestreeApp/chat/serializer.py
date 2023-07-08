from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Chat, Message

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']  


class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True,read_only=True)
    
    class Meta:
        model = Chat
        fields = '__all__'  

class ChatListSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True,read_only=True)

    class Meta:
        model = Chat
        fields = ['name','users']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,read_only=True)
     
    class Meta:
        model = Message
        fields = ['text','user','created']  







        