import asyncio
import json
from typing import Dict, List, Callable
from datetime import datetime

class WebSocketAdapter:
    def __init__(self):
        self.connections = {}
        self.channels = {}
        self._running = False
    
    async def connect(self, client_id: str, websocket):
        """Connect a new WebSocket client"""
        self.connections[client_id] = websocket
        await self.send_to_client(client_id, {
            "type": "connection",
            "status": "connected",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat()
        })
    
    async def disconnect(self, client_id: str):
        """Disconnect a WebSocket client"""
        if client_id in self.connections:
            del self.connections[client_id]
        
        # Remove from all channels
        for channel_clients in self.channels.values():
            if client_id in channel_clients:
                channel_clients.remove(client_id)
    
    async def join_channel(self, client_id: str, channel: str):
        """Join a client to a channel"""
        if channel not in self.channels:
            self.channels[channel] = []
        
        if client_id not in self.channels[channel]:
            self.channels[channel].append(client_id)
    
    async def leave_channel(self, client_id: str, channel: str):
        """Remove a client from a channel"""
        if channel in self.channels and client_id in self.channels[channel]:
            self.channels[channel].remove(client_id)
    
    async def send_to_client(self, client_id: str, message: Dict):
        """Send message to a specific client"""
        if client_id in self.connections:
            websocket = self.connections[client_id]
            try:
                await websocket.send(json.dumps(message))
            except Exception as e:
                # Connection lost, remove client
                await self.disconnect(client_id)
    
    async def broadcast_to_channel(self, channel: str, message: Dict):
        """Broadcast message to all clients in a channel"""
        if channel in self.channels:
            for client_id in self.channels[channel].copy():
                await self.send_to_client(client_id, message)
    
    async def broadcast_to_all(self, message: Dict):
        """Broadcast message to all connected clients"""
        for client_id in list(self.connections.keys()):
            await self.send_to_client(client_id, message)
    
    def simulate_investor_activity(self):
        """Simulate investor activity for demo purposes"""
        import random
        
        activities = [
            {"type": "investor_joined", "investor": "Alice Chen", "hackathon": "AI for Climate Change"},
            {"type": "funding_received", "amount": 500, "mvp": "EcoTrack AI", "backer": "GreenTech Ventures"},
            {"type": "new_message", "user": "Bob Smith", "message": "Great demo! Very promising project."},
            {"type": "investor_joined", "investor": "David Kumar", "hackathon": "FinTech Revolution"},
            {"type": "funding_received", "amount": 1000, "mvp": "CryptoLend", "backer": "Blockchain Capital"},
            {"type": "milestone_reached", "mvp": "HealthSync", "milestone": "50% funding goal reached"}
        ]
        
        return random.choice(activities)
    
    async def start_demo_activity_simulation(self):
        """Start simulating activity for demo purposes"""
        self._running = True
        while self._running:
            await asyncio.sleep(random.randint(5, 15))  # Random interval between 5-15 seconds
            
            activity = self.simulate_investor_activity()
            activity["timestamp"] = datetime.now().isoformat()
            
            # Broadcast to investor feed channel
            await self.broadcast_to_channel("investor_feed", activity)
    
    def stop_simulation(self):
        """Stop the activity simulation"""
        self._running = False
