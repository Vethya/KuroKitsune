from userbot import app, config
from .utils.parser import parse_args

from pyrogram import filters

import requests


@app.on_message(filters.outgoing & filters.text & filters.command(["udcit", "ud", "urbandictionary"], prefixes=config["prefixes"]))
async def urbandictionary(_, msg):
    chat = msg.chat
    term = " ".jooin(parse_args(msg))
    try:
        data = requests.get(f"https://api.urbandictionary.com/v0/define?term={term}").json()['list'][0]['definition'].replace("[", "").replace("]", "")
        await msg.edit_text(f"'{term}' is defined as:\n{data}")
        await msg.react(emoji="👍")
    except:
      await msg.edit_text(f"I'm unable to find a definition for '{term}'.")
      await msg.react(emoji="👎")
      
    return
