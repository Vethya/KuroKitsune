from time import time

from pyrogram.types import Message

def parse_args(msg: Message):
    text = msg.text
    return text.split()[1:]

def parse_duration(time_text: str):
    units = ["d", "h", "m"]
    if any(time_text.endswith(unit) for unit in units):
        unit = time_text[-1]
        duration = time_text[:-1]

        if not duration.isdigit():
            return "Invalid"

        duration = int(duration)
        if unit == "d":
            duration = int(time() + duration * 24 * 3600)
        elif unit == "h":
            duration = int(time() + duration * 3600)
        elif unit == "m":
            duration = int(time() + duration * 60)

        return duration
        
    else:
        return "Invalid"