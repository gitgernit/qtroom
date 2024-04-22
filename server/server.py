__all__ = []

import redis
import dotenv

import asyncio
import os

import handlers

dotenv.load_dotenv()

HOST = os.getenv('SERVER_HOST', default='localhost')
PORT = os.getenv('SERVER_PORT', default=8080)
REDIS_HOST = os.getenv('REDIS_HOST', default='localhost')
REDIS_PORT = os.getenv('REDIS_PORT', default=6379)
REDIS_DB = os.getenv('REDIS_DB', default=0)


class Server:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                                 db=REDIS_DB)

    async def startup(self):
        server = await asyncio.start_server(
            self.handle_client, HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        while True:
            data = await reader.read()

            if not data:
                writer.close()
                await writer.wait_closed()
                break

            message = data.decode()

            if message.startswith('NEWUSER'):
                answer = await handlers.handle_new_user(self, message)
                writer.write(answer.encode())
                await writer.drain()
