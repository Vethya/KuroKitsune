from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.parser import parse_args

from pyrogram import filters
from speedtest import Speedtest

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
    text += f"ID: `{entity.id}`\n"
    text += f"Name: {entity.first_name} {entity.last_name if entity.last_name else ''}\n"
    text += f"Username: @{entity.username}\n"
    text += f"Permalink: <a href='tg://user?id={entity.id}'>link</a>\n"
    text += f"Is Bot: **{entity.is_bot}**\n"
    text += f"Is Verified: **{entity.is_verified}**\n"
    text += f"Is Premium: **{entity.is_premium}**\n"

    await msg.edit_text(text)

@app.on_message(filters.outgoing & filters.text & filters.command(["speedtest", "speed"], prefixes=config["prefixes"]))
async def speedtest(_, msg):
    await msg.edit_text("`Testing...`")

    servers = []
    threads = None

    s = Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.upload(threads=threads)
    results_dict = s.results.dict()

    ping = results_dict["ping"]
    download = results_dict["download"] * (10 ** - 6) # Convert bps to mbps
    upload = results_dict["upload"] * (10 ** - 6) # Convert bps to mbps
    await msg.edit_text(
        "**Speedtest results:**\n"
        f"Ping: `{ping} ms`\n"
        f"Download speed: `{download} Mbps`\n"
        f"Upload speed: `{upload} Mbps`"
    )

CMD_TEXT = """
**Commands:**
- `{prefix}info`: Get information on the target user.
- `{prefix}speedtest` or `{prefix}speed`: Get the speedtest results of the current network using the speedtest.net API.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Misc":
            CMD_TEXT
    }
)