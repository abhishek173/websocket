from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print("websocket connected",event)
        print("Channel Layer...",self.channel_layer) # get default channel layer from project 
        print("Channel Name...",self.channel_name) # get channel name
        # Add a channel to a new or existing group 
        async_to_sync(self.channel_layer.group_add)(
            'programmers',  # group name
            self.channel_name 
            )
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print("message received from client",event['text'])
        print("Type of message received from client ",type(event['text']))
        async_to_sync(self.channel_layer.group_send)('programmers',{
            'type': 'chat.message',
            'message':event['text']
        })

    def chat_message(self,event):
        print('Event...', event)

        for i in range(10):
            self.send({
                'type':'websocket.send',
                'text': json.dumps({"count":i})
            })
            sleep(i)

    def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        print("Channel Layer...",self.channel_layer) # get default channel layer from project 
        print("Channel Name...",self.channel_name) # get channel name
        async_to_sync(self.channel_layer.group_discard)('programmers',self.channel_name)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("websocket connected",event)
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self,event):
        print("message received from client",event['text'])
        for i in range(10):
            await self.send({
                'type':'websocket.send',
                'text':json.dumps({"count":i})
            })
            await asyncio.sleep(i)

    async def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
        raise StopConsumer()
