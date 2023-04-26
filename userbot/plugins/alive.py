import sys
import time
from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX

import pyrogram
from pyrogram import filters

@app.on_message(filters.outgoing & filters.text & filters.command(["start", "alive"], prefixes=config["prefixes"]))
async def alive(_, msg):
    python_ver = sys.version_info
    await msg.edit_text(
        "**KuroKitsune is online!**\n" +
        f"Python version: `{python_ver.major}.{python_ver.minor}.{python_ver.micro}`\n" +
        f"Pyrogram version: `{pyrogram.__version__}`"
    )

@app.on_message(filters.outgoing & filters.text & filters.command(["ping"], prefixes=config["prefixes"]))
async def ping(_, msg):
    start = time.time()
    await msg.edit_text("`Pinging...`")
    end = time.time()

    latency = int((end - start) * 1000)
    await msg.edit_text(
        "**Pong!**\n" +
        f"`{latency}` ms"
    )

CMD_TEXT = """
**Commands:**
- `{prefix}start` or `{prefix}alive`: Check if KuroKitsune is alive and also contains additional information.
- `{prefix}ping`: See KuroKitsune ping.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Alive":
            CMD_TEXT
    }
)