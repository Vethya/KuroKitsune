from userbot import app, config
from .utils.parser import parse_args

from pyrogram import filters

import requests


@app.on_message(filters.outgoing & filters.text & filters.command(["udcit", "ud", "urbandictionary"], prefixes=config["prefixes"]))
async def urbandictionary(_, msg):
    chat = msg.chat
    term = " ".join(parse_args(msg))
    try:
        data = requests.get(f"https://api.urbandictionary.com/v0/define?term={term}").json()['list'][0]
        definition = data['definition'].replace("[", "").replace("]", "")
        example = data['example'].replace("[", "").replace("]", "")
        thumbs_up = data['thumbs_up']
        thumbs_down = data['thumbs_down']
        await msg.edit_text(f"'{term}' is defined as:\n{definition}\nExample usage:\n__{example}__\nDefinition rating: 👍{thumbs_up}/👎{thumbs_down}")
    except:
      await msg.edit_text(f"I'm unable to find a definition for '{term}'.")
      
    return
