from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='user_chats')
    name = models.CharField(max_length=20, null=True)

class Message(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_messages')
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='chat_messages')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']