from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.auth import database_sync_to_async
from .models import Chat,Group
import json

   


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        print(self.groupname)
        # to add a channel in a statis group 
        await self.channel_layer.group_add(
            self.groupname,  # group name
            self.channel_name   # channel name
            )
        

        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):
        if self.scope['user'].is_authenticated:
            data = json.loads(event['text'])
            if data['msg']:

                # Find Group Name 
                group = await database_sync_to_async(Group.objects.get)(name=self.groupname)

                chat = Chat(user=self.scope['user'],content = data['msg'],group=group)
                await database_sync_to_async(chat.save)()

                data['user'] = self.scope['user'].username
                data['f_name'] = self.scope['user'].first_name
                data['l_name'] = self.scope['user'].last_name

                await self.channel_layer.group_send(self.groupname,
                {
                    'type': 'chat.message',
                    'message': json.dumps(data),
                }
                    )
            else:
                await self.send({
                    'type':'websocket.send',
                    'text':json.dumps({'msg':'Message can not be empty','user':self.scope['user'].username})
                })
        else:
            await self.send({
                'type':'websocket.send',
                'text':json.dumps({'msg':'Login Required','user':'Guestuser'})
            })
    
    async def chat_message(self, event):
        await self.send({
            'type':'websocket.send',
            'text': event['message'],
        })


    async def websocket_disconnect(self, event):
        # to discard a channel from a statis group 
        await self.channel_layer.group_discard(
            self.groupname,  # group name
            self.channel_name  # channel name
            )

        raise StopConsumer()
    