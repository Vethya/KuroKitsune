from userbot import app, config, HELP_DICT, FIRST_CMD_PREFIX
from .utils.permissions import is_admin
from .utils.parser import parse_args, parse_duration
from .utils.fetcher import get_user

from pyrogram import filters
from pyrogram.types import ChatPermissions


@app.on_message(filters.outgoing & filters.text & filters.command(["kick"], prefixes=config["prefixes"]))
async def kick(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("<b>Invalid Username or ID</b>")
        return

    if user.id == msg.from_user.id:
        await msg.edit_text("Please don't kick yourself. Please use <b>.leave</b> instead, if you want to leave")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("<b>Insufficient Permission</b>")
        return

    try:
        await chat.kick_member(user.id)
        await chat.unban_member(user.id)
    except:
        await msg.edit_text("<b>Failed to kick user</b>")
        return

    await msg.edit_text(f"Kicked <b>{user.first_name}</b> from <b>{chat.title}</b>")

@app.on_message(filters.outgoing & filters.text & filters.command(["ban"], prefixes=config["prefixes"]))
async def ban(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("<b>Invalid Username or ID</b>")
        return

    if user.id == msg.from_user.id: 
        await msg.edit_text("Please don't ban yourself. Please use <b>.leave</b> instead, if you want to leave")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("<b>Insufficient Permission</b>")
        return

    time_text = args[1]
    if time_text:
        duration = parse_duration(time_text)

        try:
            await chat.kick_member(user.id, duration)
        except:
            await msg.edit_text("<b>Failed to ban user</b>")
            return
        await msg.edit_text(f"Banned <b>{user.first_name}</b> from <b>{chat.title}</b> for {time_text}")

    else:
        try:
            await chat.kick_member(user.id)
        except:
            await msg.edit_text("<b>Failed to ban user</b>")
            return
        await msg.edit_text(f"Banned <b>{user.first_name}</b> from <b>{chat.title}</b>")

@app.on_message(filters.outgoing & filters.text & filters.command(["unban"], prefixes=config["prefixes"]))
async def unban(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("<b>Invalid Username or ID</b>")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("<b>Insufficient Permission</b>")
        return
    
    try:
        member = await chat.get_member(user.id)
    except:
        await msg.edit_text("<b>Invalid Member</b>")
        return

    if member.status not in ("left", "kicked"):
        await msg.edit("<b>User is not banned</b>")
        return

    try:
        await chat.unban_member(user.id)
    except:
        await msg.edit_text("<b>Failed to unban user</b>")
        return
    await msg.edit_text(f"Unbanned <b>{user.first_name}</b> in <b>{chat.title}</b>")

@app.on_message(filters.outgoing & filters.text & filters.command(["mute"], prefixes=config["prefixes"]))
async def mute(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("<b>Invalid Username or ID</b>")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("<b>Insufficient Permission</b>")
        return

    time_text = args[1]
    if time_text:
        duration = parse_duration(time_text)

        try:
            await chat.restrict_member(user.id, ChatPermissions(can_send_messages=False), duration)
        except:
            await msg.edit_text("<b>Failed to mute user</b>")
            return
        await msg.edit_text(f"Muted <b>{user.first_name}</b> in <b>{chat.title}</b> for {time_text}")

    else:
        try:
            await chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
        except:
            await msg.edit_text("<b>Failed to mute user</b>")
            return
        await msg.edit_text(f"Muted <b>{user.first_name}</b> in <b>{chat.title}</b>")

@app.on_message(filters.outgoing & filters.text & filters.command(["unmute"], prefixes=config["prefixes"]))
async def unmute(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("<b>Invalid Username or ID</b>")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("<b>Insufficient Permission</b>")
        return
    
    try:
        member = await chat.get_member(user.id)
    except:
        await msg.edit_text("<b>Invalid Member</b>")
        return

    if member.can_send_messages:
        await msg.edit("<b>User is not muted</b>")
        return

    try:
        await chat.restrict_member(user.id, ChatPermissions(can_send_messages=True))
    except:
        await msg.edit_text("<b>Failed to unmute user</b>")
        return
    await msg.edit_text(f"Unmuted <b>{user.first_name}</b> in <b>{chat.title}</b>")

@app.on_message(filters.outgoing & filters.text & filters.command(["leave"], prefixes=config["prefixes"]))
async def leave(_, msg):
    chat = msg.chat

    await msg.edit_text("<b>This chat is not cool. Bye!</b>")
    await chat.leave()
    
CMD_TEXT = """
<b>Commands:</b>"
- <code>{prefix}kick</code>: Kick a user from a group.
- <code>{prefix}ban</code>: Ban a user from a group.
- <code>{prefix}unban</code>: Unban a user in a group.
- <code>{prefix}mute</code>: Mute a user in a group.
- <code>{prefix}unmute</code>: Unmute a user in a group.
- <code>{prefix}leave</code>: Leave a group.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Chat":
            CMD_TEXT
    }
)