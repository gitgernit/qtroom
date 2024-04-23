import asyncio

import server

server = server.Server()


async def main():
    await server.startup()


if __name__ == '__main__':
    asyncio.run(main())
