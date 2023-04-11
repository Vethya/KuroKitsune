import json
import os

from pyrogram import Client

HELP_DICT = {}

with open("config.json", "r") as file:
    config = json.load(file)

app = Client(
    "KuroKitsune",
    api_id=config["api_id"],
    api_hash=config["api_hash"],
    plugins={'root': os.path.join(__package__, 'plugins')},
)