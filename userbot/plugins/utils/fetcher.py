from userbot import app

async def get_user(user):
    if user.startswith("@"):
        user = user[1:]

    return await app.get_users(user)