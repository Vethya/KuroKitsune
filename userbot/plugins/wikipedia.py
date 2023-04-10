from userbot import app, config
from .utils.parser import parse_args

from pyrogram import filters

import wikipediaapi

@app.on_message(filters.outgoing & filters.text & filters.command(["wikipedia"], prefixes=config["prefixes"]))
async def wikipedia(_, msg):
    chat = msg.chat
    term = " ".join(parse_args(msg))
    try:
        page = wikipediaapi.page(term)
        msg. edit_text(f"Here is the Wikipedia summary for {term}:\n{page.summary}\nYou can find more information on {page.title} [here]({page.fullurl}) ")
    except:
        await msg.edit_text(f"I'm unable to find a wikipedia entry for '{term}'.")
