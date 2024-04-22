import server
import asyncio

server = server.Server()


async def main():
    await server.startup()


if __name__ == '__main__':
    asyncio.run(main())
