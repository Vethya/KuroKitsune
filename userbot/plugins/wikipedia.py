from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.parser import parse_args

from pyrogram import filters

import wikipediaapi

@app.on_message(filters.outgoing & filters.text & filters.command(["wiki", "wikipedia"], prefixes=config["prefixes"]))
async def wikipedia(_, msg):
    term = " ".join(parse_args(msg))
    wiki = wikipediaapi.Wikipedia('en')

    try:
        page = wiki.page(term)
        await msg.edit_text(f"**Here is the Wikipedia summary for {term}:**\n{page.summary}\n\nYou can find more information on {page.title} [here]({page.fullurl}).")
    except:
        await msg.edit_text(f"I'm unable to find a wikipedia entry for '{term}'.")

CMD_TEXT = """
**Commands:**
- `{prefix}wiki` or `{prefix}wikipedia`: Get a Wikipedia summary of a query on Wikipedia.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Wikipedia":
            CMD_TEXT
    }
)