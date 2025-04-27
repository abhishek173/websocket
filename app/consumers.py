from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event):
        print("websocket connected",event)
        self.send({
            'type':'websocket.accept'
        })

    def websocket_receive(self,event):
        print("message received from client",event['text'])
        for i in range(10):
            self.send({
                'type':'websocket.send',
                'text': json.dumps({"count":i})
            })
            sleep(i)

    def websocket_disconnect(self,event):
        print("Websocket Disconnected...",event)
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
