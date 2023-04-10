from userbot import app, config
from .utils.parser import parse_args

from pyrogram import filters

import wikipediaapi

@app.on_message(filters.outgoing & filters.text & filters.command(["wiki", "wikipedia"], prefixes=config["prefixes"]))
async def wikipedia(_, msg):
    term = " ".join(parse_args(msg))
    wiki = wikipediaapi.Wikipedia('en')

    try:
        page = wiki.page(term)
        await msg.edit_text(f"<b>Here is the Wikipedia summary for {term}:</b>\n{page.summary}\n\nYou can find more information on {page.title} [here]({page.fullurl}).")
    except:
        await msg.edit_text(f"I'm unable to find a wikipedia entry for '{term}'.")
