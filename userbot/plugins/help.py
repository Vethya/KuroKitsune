from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.parser import parse_args

from pyrogram import filters

@app.on_message(filters.outgoing & filters.text & filters.command(["help"], prefixes=config["prefixes"]))
async def help_(_, msg):
    args = parse_args(msg)

    try:
        plugin = args[0]

        if plugin in HELP_DICT:
            await msg.edit_text(f"Help for **{plugin}**:\n\n{HELP_DICT[plugin]}")
        else:
            await msg.edit_text(f"No plugin found with the name **{plugin}**.")
            return
    except IndexError:
        text = "Here are the help for all available plugins:\n"
        for plugin in sorted(HELP_DICT):
            text += f"- `{plugin}`\n"

        await msg.edit_text(text)

CMD_TEXT = """
**Commands:**
- `{prefix}help` or `{prefix} <cmd>`: Get a list of all plugins or a help for each one.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "help":
            CMD_TEXT
    }
)