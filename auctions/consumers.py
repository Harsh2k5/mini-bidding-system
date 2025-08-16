import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f'auction_{self.auction_id}'
        await self.channel_layer.group_add(self.auction_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.auction_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('type') == 'new_bid':
            await self.channel_layer.group_send(
                self.auction_group_name,
                {'type': 'bid_update', 'amount': text_data_json['amount'], 'bidder': text_data_json['bidder']}
            )

    async def bid_update(self, event):
        await self.send(text_data=json.dumps(event))
