import client
import asyncio

connection = client.Connection()


async def main():
    await connection.connect()
    await connection.send('halo')


if __name__ == '__main__':
    asyncio.run(main())
