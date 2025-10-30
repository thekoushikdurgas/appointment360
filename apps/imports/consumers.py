"""
WebSocket consumers for import progress
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from apps.imports.models import ImportJob


class ImportProgressConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time import progress"""
    
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = f'import_{self.job_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        data = json.loads(text_data)
        message = data['message']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        """Receive message from room group"""
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def import_progress(self, event):
        """Handle import progress updates"""
        data = event['data']
        
        # Send progress update to WebSocket
        await self.send(text_data=json.dumps(data))

