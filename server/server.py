__all__ = []

import asyncio
import json
import os

import dotenv
import handlers
import redis

dotenv.load_dotenv()

HOST = os.getenv('SERVER_HOST', default='localhost')
PORT = os.getenv('SERVER_PORT', default=8080)
REDIS_HOST = os.getenv('REDIS_HOST', default='localhost')
REDIS_PORT = os.getenv('REDIS_PORT', default=6379)
REDIS_DB = os.getenv('REDIS_DB', default=0)


class Server:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.clients = []
        self.writers = {}

    async def startup(self):
        server = await asyncio.start_server(self.handle_client, HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        if (
            reader,
            writer,
        ) not in self.clients:
            self.clients.append(
                (reader, writer),
            )

        while True:
            try:
                data = await reader.read(1024)

            except ConnectionResetError:
                await self.destroy_client(reader, writer)
                break

            if not data:
                await self.destroy_client(reader, writer)
                break

            message = json.loads(data.decode())

            match message['type']:
                case 'connection':
                    validity, token = await handlers.handle_new_user(
                        self,
                        message,
                    )
                    data = {
                        'type': 'connection',
                        'valid': validity,
                        'token': str(token),
                    }

                    if token:
                        self.writers[writer] = str(token)

                    writer.write(json.dumps(data).encode())
                    await writer.drain()

                case 'message':
                    if await handlers.message_is_valid(self, message['token']):
                        username = self.redis.hget(
                            message['token'],
                            'username',
                        ).decode()
                        msg = message['message']
                        data = {
                            'type': 'message',
                            'username': username,
                            'message': msg,
                        }

                    for client in self.clients:
                        client[1].write(json.dumps(data).encode())
                        await client[1].drain()

    async def destroy_client(self, reader, writer):
        self.redis.delete(self.writers.get(writer, ''))

        self.clients.pop(self.clients.index((reader, writer)))
        self.writers.pop(writer, None)

        writer.close()
