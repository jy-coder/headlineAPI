from channels.generic.websocket import AsyncJsonWebsocketConsumer,AsyncConsumer

class IndexConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("connected")
        # await self.channel_layer.group_add('index', self.channel_name)

    async def disconnect(self, code):
        print('disconnected')
        # await self.channel_layer.group_discard('index', self.channel_name)
        # print(f'removed {self.channel_name}')

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        # print("here")
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
       