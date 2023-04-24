from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.parser import parse_args

from pyrogram import filters

from gpytranslate import Translator

@app.on_message(filters.outgoing & filters.text & filters.command(["translate", "tr", "tl"], prefixes=config["prefixes"]))
async def translate(_, msg):
    args = parse_args(msg)

    t = Translator()
    if len(args) == 1:
        reply = msg.reply_to_message
        if reply:
            lang = args[0]
            sentence = reply.text

            translation = await t.translate(sentence, targetlang=lang)
            sentence_lang = await t.detect(sentence)

            await msg.edit_text(
                f"<b>Translated</b> ({sentence_lang}-{lang})\n"
                f"<code>{translation.text}</code>"
            )

        else:
            await msg.edit_text("Reply to a message or provide a sentence.")
            return
    
    elif len(args) > 2:
        source_lang = args[0]
        target_lang = args[1]
        sentence = args[2]

        translation = await t.translate(sentence, sourceLang=source_lang, targetlang=target_lang)

        await msg.edit_text(
            f"<b>Translated</b> ({source_lang}-{target_lang})\n"
            f"<code>{translation.text}</code>"
        )
    
    else:
        lang = args[0]
        sentence = args[1]

        translation = await t.translate(sentence, targetlang=lang)
        sentence_lang = await t.detect(sentence)

        await msg.edit_text(
            f"<b>Translated</b> ({sentence_lang}-{lang})\n"
            f"<code>{translation.text}</code>"
        )

CMD_TEXT = """
<b>Commands:</b>
- <code>{prefix}tr</code> or <code>{prefix}tl</code> or <code>{prefix}translate</code> <source> <target> <sentence>: 
Get a translation of a sentence on Google Translate. Source can be omitted for autodetect and target can also be omitted if you reply.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Wikipedia":
            CMD_TEXT
    }
)