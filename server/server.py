__all__ = []

import asyncio
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
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                                 db=REDIS_DB)
        self.clients = []

    async def startup(self):
        server = await asyncio.start_server(
            self.handle_client, HOST, PORT)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        if (reader, writer) not in self.clients:
            self.clients.append((reader, writer))

        while True:
            data = await reader.read(1024)

            if not data:
                self.clients.pop(self.clients.index((reader, writer)))
                writer.close()
                await writer.wait_closed()
                break

            message = data.decode()

            if message.startswith('NEWUSER'):
                answer = await handlers.handle_new_user(self, message)
                writer.write(answer.encode())
                await writer.drain()

            else:
                for client in self.clients:
                    client[1].write(message.encode())
                    await client[1].drain()
