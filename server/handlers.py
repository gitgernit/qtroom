import uuid


async def handle_new_user(server, message):
    username = message['username']

    keys = server.redis.keys('*')

    for key in keys:
        if server.redis.hget(key, 'username').decode() == username:
            return False, ''

    user_id = uuid.uuid4()
    server.redis.hset(str(user_id), mapping={'username': username})

    return True, user_id


async def message_is_valid(server, token):
    if server.redis.exists(token):
        return True

    else:
        return False
