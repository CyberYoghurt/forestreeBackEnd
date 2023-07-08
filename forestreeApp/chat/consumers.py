import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Chat, Message
from .serializer import MessageSerializer



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.room_name= self.scope["url_route"]["kwargs"]["room_name"]

            self.room_group_name = "chat_%s" % self.room_name

            # Add this channel to a group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            # Getting a chat
            try:
                 
                 self.active_chat = Chat.objects.get(name=self.room_name)
            except Exception as E:
                self.active_chat = Chat.objects.create(name=self.room_name)

            #Getting and serialing messages of the active chat
            self.user = self.scope['user']
            messages = self.active_chat.chat_messages
            serialized_messages = MessageSerializer(messages,many=True)
            self.accept()
            

            self.send(text_data=json.dumps({
                    'content':serialized_messages.data
                    })) 
        
        except Exception as E:
            print(E)
    


    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        if(self.scope['user'].is_anonymous):
            self.send(text_data=json.dumps({
                'status' :False,
                'content':'Sign to send messages'
                })) 
            return
        data = json.loads(text_data)
        message = data['message']
        new_message = Message(chat = self.active_chat, user = self.user, text = message)
        new_message.save()
        message_serialized = MessageSerializer(new_message,many=False)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message_serialized.data}
        ) 
        return

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"content": message}))
        

