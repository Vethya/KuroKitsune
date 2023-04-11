from userbot import app, config, HELP_DICT
from .utils.parser import parse_args

from pyrogram import filters

import requests


@app.on_message(filters.outgoing & filters.text & filters.command(["udict", "ud", "urbandictionary"], prefixes=config["prefixes"]))
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

HELP_DICT.update(
   {
      "Dictionary":
          "<b>Commands:</b>\n"
          "- /udict or /ud or /urbandictionary: Get a definition of a query on Urban Dictionary.\n"
   }
)