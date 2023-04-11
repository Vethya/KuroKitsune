import sys
import time
from userbot import app, config, HELP_DICT

import pyrogram
from pyrogram import filters

@app.on_message(filters.outgoing & filters.text & filters.command(["start", "alive"], prefixes=config["prefixes"]))
async def alive(_, msg):
    python_ver = sys.version_info
    await msg.edit_text(
        "<b>KuroKitsune is online!</b>\n" +
        f"Python version: <code>{python_ver.major}.{python_ver.minor}.{python_ver.micro}</code>\n" +
        f"Pyrogram version: <code>{pyrogram.__version__}</code>"
    )

@app.on_message(filters.outgoing & filters.text & filters.command(["ping"], prefixes=config["prefixes"]))
async def ping(_, msg):
    start = time.time()
    await msg.edit_text("<b>Pinging...</b>")
    end = time.time()

    latency = int((end - start) * 1000)
    await msg.edit_text(
        "<b>Pong!</b>\n" +
        f"<code>{latency}</code> ms"
    )



HELP_DICT.update(
    {
        "Alive":
            "<b>Commands:</b>\n"
            "- /start or /alive: Check if KuroKitsune is alive and also contains additional information.\n"
            "- /ping: See KuroKitsune ping.\n"
    }
)