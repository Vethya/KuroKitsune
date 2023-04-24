import json
import os

from pyrogram import Client

with open("config.json", "r") as file:
    config = json.load(file)

HELP_DICT = {}
FIRST_CMD_PREFIX = config["prefixes"][0]

app = Client(
    "KuroKitsune",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    plugins={'root': os.path.join(__package__, 'plugins')},
)