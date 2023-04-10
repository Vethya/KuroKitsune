from userbot import app, config
from .utils.parser import parse_args

from pyrogram import filters

import requests
import wikipedia


@app.on_message(filters.outgoing & filters.text & filters.command(["udcit", "ud", "urbandictionary"], prefixes=config["prefixes"]))
async def urbandictionary(_, msg):
    term = " ".join(parse_args(msg))

    try:
        data = requests.get(f"https://api.urbandictionary.com/v0/define?term={term}").json()['list'][0]
        definition = data['definition'].replace("[", "").replace("]", "")
        example = data['example'].replace("[", "").replace("]", "")
        thumbs_up = data['thumbs_up']
        thumbs_down = data['thumbs_down']
        await msg.edit_text(f"<b>'{term}' is defined as:</b>\n{definition}\n\n<b>Example usage:</b>\n__{example}__\n\n<b>Rating:</b> 👍{thumbs_up} 👎{thumbs_down}")
    except:
      await msg.edit_text(f"I'm unable to find a definition for '{term}'.")
      
    return

@app.on_message(filters.outgoing & filters.text & filters.command(["wikipedia"], prefixes=config["prefixes"]))
async def wikipedia(_, msg):
    chat = msg.chat
    term = " ".join(parse_args(msg))
    try:
        page = wikipedia.page(term)
        msg.edit_text(f"Here is the Wikipedia summary for {term}:\n{page.summary}\nYou can find more information on {page.title} [here]({page.url}) ")
    except:
        await msg.edit_text(f"I'm unable to find a wikipedia entry for '{term}'.")
