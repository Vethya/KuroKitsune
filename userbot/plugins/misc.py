from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.parser import parse_args

from pyrogram import filters

@app.on_message(filters.outgoing & filters.text & filters.command(["info",  "user", "whois"], prefixes=config["prefixes"]))
async def info(_, msg):
    args = parse_args(msg)

    try:
        try:
            entity = int(args[0])
        except ValueError:
            entity = args[0]
    
    except IndexError:
        reply = msg.reply_to_message
        if reply:
            entity = reply.from_user
        else:
            entity = msg.from_user

    if isinstance(entity, (str, int)):
        try:
            entity = await app.get_users(entity)
        except:
            await msg.edit_text("User not found.")
            return

    text = f"USER INFO:\n\n"
    text += f"ID: <code>{entity.id}</code>\n"
    text += f"Name: {entity.first_name} {entity.last_name if entity.last_name else ''}\n"
    text += f"Username: @{entity.username}\n"
    text += f"Permalink: <a href='tg://user?id={entity.id}'>link</a>\n"
    text += f"Is Bot: <b>{entity.is_bot}</b>\n"
    text += f"Is Verified: <b>{entity.is_verified}</b>\n"
    text += f"Is Premium: <b>{entity.is_premium}</b>\n"

    await msg.edit_text(text)

CMD_TEXT = """
<b>Commands:</b>
- <code>{prefix}info</code>: Get information on the target user.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Misc":
            CMD_TEXT
    }
)