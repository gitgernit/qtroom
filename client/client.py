__all__ = []

import asyncio
import os
import typing

import dotenv

dotenv.load_dotenv()

HOST = os.getenv('SERVER_HOST', default='localhost')
PORT = os.getenv('SERVER_PORT', default=8080)


class Connection:
    def __init__(self, ui):
        self.reader: typing.Optional[asyncio.StreamReader] = None
        self.writer: typing.Optional[asyncio.StreamWriter] = None
        self.ui = ui

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            HOST, PORT)
        listen_task = asyncio.create_task(self.listen())

    async def listen(self):
        while True:
            data = await self.reader.read(1024)
            message = data.decode()
            self.ui.textEdit.insertPlainText(f'{message}\n')

    async def send(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()
