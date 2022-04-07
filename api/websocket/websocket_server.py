import asyncio
import websockets
from werkzeug.routing import Map

from metaclass import SingletonMeta

sio = socketio.Server()
