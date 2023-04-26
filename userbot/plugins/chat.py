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
        await msg.edit_text("**Invalid Username or ID**")
        return

    if user.id == msg.from_user.id:
        await msg.edit_text("Please don't kick yourself. Please use `.leave` instead, if you want to leave")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("**Insufficient Permission**")
        return

    try:
        await chat.kick_member(user.id)
        await chat.unban_member(user.id)
    except:
        await msg.edit_text("**Failed to kick user**")
        return

    await msg.edit_text(f"Kicked **{user.first_name}** from **{chat.title}**")

@app.on_message(filters.outgoing & filters.text & filters.command(["ban"], prefixes=config["prefixes"]))
async def ban(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("**Invalid Username or ID**")
        return

    if user.id == msg.from_user.id: 
        await msg.edit_text("Please don't ban yourself. Please use `.leave` instead, if you want to leave")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("**Insufficient Permission**")
        return

    time_text = args[1]
    if time_text:
        duration = parse_duration(time_text)

        try:
            await chat.kick_member(user.id, duration)
        except:
            await msg.edit_text("**Failed to ban user**")
            return
        await msg.edit_text(f"Banned **{user.first_name}** from **{chat.title}** for {time_text}")

    else:
        try:
            await chat.kick_member(user.id)
        except:
            await msg.edit_text("**Failed to ban user**")
            return
        await msg.edit_text(f"Banned **{user.first_name}** from **{chat.title}**")

@app.on_message(filters.outgoing & filters.text & filters.command(["unban"], prefixes=config["prefixes"]))
async def unban(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("**Invalid Username or ID**")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("**Insufficient Permission**")
        return
    
    try:
        member = await chat.get_member(user.id)
    except:
        await msg.edit_text("**Invalid Member**")
        return

    if member.status not in ("left", "kicked"):
        await msg.edit("**User is not banned**")
        return

    try:
        await chat.unban_member(user.id)
    except:
        await msg.edit_text("**Failed to unban user**")
        return
    await msg.edit_text(f"Unbanned **{user.first_name}** in **{chat.title}**")

@app.on_message(filters.outgoing & filters.text & filters.command(["mute"], prefixes=config["prefixes"]))
async def mute(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("**Invalid Username or ID**")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("**Insufficient Permission**")
        return

    time_text = args[1]
    if time_text:
        duration = parse_duration(time_text)

        try:
            await chat.restrict_member(user.id, ChatPermissions(can_send_messages=False), duration)
        except:
            await msg.edit_text("**Failed to mute user**")
            return
        await msg.edit_text(f"Muted **{user.first_name}** in **{chat.title}** for {time_text}")

    else:
        try:
            await chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
        except:
            await msg.edit_text("**Failed to mute user**")
            return
        await msg.edit_text(f"Muted **{user.first_name}** in **{chat.title}**")

@app.on_message(filters.outgoing & filters.text & filters.command(["unmute"], prefixes=config["prefixes"]))
async def unmute(_, msg):
    chat = msg.chat
    args = parse_args(msg)
    try:
        user = await get_user(args[0])
    except:
        await msg.edit_text("**Invalid Username or ID**")
        return

    if not await is_admin(chat.id, msg.from_user.id):
        await msg.edit_text("**Insufficient Permission**")
        return
    
    try:
        member = await chat.get_member(user.id)
    except:
        await msg.edit_text("**Invalid Member**")
        return

    if member.can_send_messages:
        await msg.edit("**User is not muted**")
        return

    try:
        await chat.restrict_member(user.id, ChatPermissions(can_send_messages=True))
    except:
        await msg.edit_text("**Failed to unmute user**")
        return
    await msg.edit_text(f"Unmuted **{user.first_name}** in **{chat.title}**")

@app.on_message(filters.outgoing & filters.text & filters.command(["leave"], prefixes=config["prefixes"]))
async def leave(_, msg):
    chat = msg.chat

    await msg.edit_text("This chat is not cool. Bye!")
    await chat.leave()
    
CMD_TEXT = """
**Commands:**"
- `{prefix}kick`: Kick a user from a group.
- `{prefix}ban`: Ban a user from a group.
- `{prefix}unban`: Unban a user in a group.
- `{prefix}mute`: Mute a user in a group.
- `{prefix}unmute`: Unmute a user in a group.
- `{prefix}leave`: Leave a group.
""".strip().format(prefix = FIRST_CMD_PREFIX)

HELP_DICT.update(
    {
        "Chat":
            CMD_TEXT
    }
)