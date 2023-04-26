from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
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
        await msg.edit_text(f"**{term} is defined as:**\n{definition}\n\n**Example usage:**\n__{example}__\n\n**Rating:** 👍{thumbs_up} 👎{thumbs_down}")
    except:
      await msg.edit_text(f"I'm unable to find a definition for {term}.")
      
    return

@app.on_message(filters.outgoing & filters.text & filters.command(["jisho"], prefixes=config["prefixes"]))
async def jisho(_, msg):
    term = " ".join(parse_args(msg))

    data = requests.get(f"https://jisho.org/api/v1/search/words?keyword={term}").json()["data"]
    if len(data) == 0:
        await msg.edit_text("No results found.")
        return
    data = data[0]

    if data['japanese'][0]['reading']:
        text = f"**Japanese:** {data['japanese'][0]['reading']}\n"
    elif data['japanese'][0]['word']:
        text = f"**Japanese:** {data['japanese'][0]['word']}\n"
    elif (data['japanese'][0]['reading'], data['japanese'][0]['word']):
        text = f"**Japanese:** {data['japanese'][0]['reading']} ({data['japanese'][0]['word']})\n"

    senses = data["senses"]
    if len(senses) > 1:
        for sense in senses:
            eng_defs = sense['english_definitions']
            text += f"- {', '.join(eng_defs)}\n" if len(eng_defs) > 1 else f"- {eng_defs[0]}\n"
    else:
        text += f"- {senses[0]['english_definitions']}\n"

    await msg.edit_text(text)
    return

CMD_TEXT = """
**Commands:**
- `{prefix}udict` or `{prefix}ud` or `{prefix}urbandictionary`: Get a definition of a query on Urban Dictionary.
- `{prefix}jisho`: Get a japanese definition of a query on jisho.org.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
   {
        "Dictionary":
            CMD_TEXT
   }
)