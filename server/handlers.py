async def handle_new_user(server, message):
    username = message.split()[-1]

    if server.redis.exists(username):
        return 'taken'

    return 'valid'
