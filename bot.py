from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import (
    add_user,
    add_group,
    all_users,
    all_groups,
    users,
    remove_user,
    add_sudo,
    remove_sudo,
    get_sudolist,
)
from configs import cfg
import random, asyncio, os, sys

def is_sudo(user_id: int) -> bool:
    return user_id == cfg.OWNER_ID or user_id in cfg.SUDO or user_id in get_sudolist()
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.messenger").setLevel(logging.ERROR)

app = Client(
    "approver", api_id=cfg.API_ID, api_hash=cfg.API_HASH, bot_token=cfg.BOT_TOKEN
)

gif = [
    "https://telegra.ph/file/a5a2bb456bf3eecdbbb99.mp4",
    "https://telegra.ph/file/03c6e49bea9ce6c908b87.mp4",
    "https://telegra.ph/file/9ebf412f09cd7d2ceaaef.mp4",
    "https://telegra.ph/file/293cc10710e57530404f8.mp4",
    "https://telegra.ph/file/506898de518534ff68ba0.mp4",
    "https://telegra.ph/file/dae0156e5f48573f016da.mp4",
    "https://telegra.ph/file/3e2871e714f435d173b9e.mp4",
    "https://telegra.ph/file/714982b9fedfa3b4d8d2b.mp4",
    "https://telegra.ph/file/876edfcec678b64eac480.mp4",
    "https://telegra.ph/file/6b1ab5aec5fa81cf40005.mp4",
    "https://telegra.ph/file/b4834b434888de522fa49.mp4",
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(
            kk.id,
            img,
            "**Hello {}!\nWelcome To {}\n\n__Powered By : @rs_bro__**".format(
                m.from_user.mention, m.chat.title
            ),
        )
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("start"))
async def op(_, m: Message):
    if cfg.CHID:
        try:
            chat_target = cfg.FSUB.strip().replace("@", "") if cfg.FSUB else cfg.CHID
            try:
                await app.get_chat_member(chat_target, m.from_user.id)
            except Exception:
                await app.get_chat_member(cfg.CHID, m.from_user.id)
        except UserNotParticipant:
            key = InlineKeyboardMarkup([[InlineKeyboardButton("🍀 Check Again 🍀", "chk")]])
            await m.reply_text(
                "**⚠️Access Denied!⚠️\n\nPlease Join @{} to use me.If you joined click check again button to confirm.**".format(
                    cfg.FSUB
                ),
                reply_markup=key,
            )
            return
        except Exception as e:
            logging.error(f"Error checking chat member for force subscribe: {e}")

    try:
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🗯 Channel", url="https://telegram.me/rs_bro"
                        ),
                        InlineKeyboardButton(
                            "💬 Admin", url="https://telegram.me/rs_m_bot"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "➕ Add me to your Chat ➕",
                            url="https://telegram.me/rs_approval_bot?startgroup",
                        )
                    ],
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo(
                "https://graph.org/file/feaf97c1872228fc44dfb.png",
                caption="**🦊 Hello {}!\nI'm RS Auto Approval Bot that works on this [telegram feature]({}).\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @rs_bro__**".format(
                    m.from_user.mention, "https://t.me/telegram/153"
                ),
                reply_markup=keyboard,
            )

        elif m.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💁‍♂️ Start me private 💁‍♂️",
                            url="https://telegram.me/rs_approval_bot?start=start",
                        )
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text(
                "**🦊 Hello {}!\nwrite me in private for more details**".format(
                    m.from_user.first_name
                ),
                reply_markup=keyboar,
            )
        print(m.from_user.first_name + " started Your Bot!")
    except Exception as err:
        logging.error(f"Error in start command handler: {err}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    if cfg.CHID:
        try:
            chat_target = cfg.FSUB.strip().replace("@", "") if cfg.FSUB else cfg.CHID
            try:
                await app.get_chat_member(chat_target, cb.from_user.id)
            except Exception:
                await app.get_chat_member(cfg.CHID, cb.from_user.id)
        except UserNotParticipant:
            await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️", show_alert=True)
            return
        except Exception as e:
            logging.error(f"Error checking chat member in callback: {e}")

    try:
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🗯 Channel", url="https://telegram.me/rs_bro"
                        ),
                        InlineKeyboardButton(
                            "💬 Support", url="https://telegram.me/rs_m_bot"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "➕ Add me to your Chat ➕",
                            url="https://telegram.me/rs_approval_bot?startgroup",
                        )
                    ],
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit(
                "**🦊 Hello {}!\nI'm RS Auto Approval Bot that works on this [telegram feature]({}).\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @rs_bro__**".format(
                    cb.from_user.mention, "https://t.me/telegram/153"
                ),
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        print(cb.from_user.first_name + " started Your Bot!")
    except Exception as err:
        logging.error(f"Error in chk callback query handler: {err}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("users"))
async def dbtool(_, m: Message):
    if not m.from_user or not is_sudo(m.from_user.id):
        await m.reply_text("🔒 **Permission Denied**\n\n__You are not an admin! These commands work with admin or owner only.__")
        return
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(
        text=f"""📊 **RS Auto Approval Stats** 📊

┌──🙋‍♂️ **Total Users:** `{xx}`
├──👥 **Total Groups:** `{x}`
└──🚧 **Grand Total:** `{tot}`

__Powered By : @rs_bro__"""
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("bcast"))
async def bcast(_, m: Message):
    if not m.from_user or not is_sudo(m.from_user.id):
        await m.reply_text("🔒 **Permission Denied**\n\n__You are not an admin! These commands work with admin or owner only.__")
        return
    if not m.reply_to_message:
        await m.reply_text("❌ **Please reply to a message to broadcast!**")
        return
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            # print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(
        f"✅Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("fcast"))
async def fcast(_, m: Message):
    if not m.from_user or not is_sudo(m.from_user.id):
        await m.reply_text("🔒 **Permission Denied**\n\n__You are not an admin! These commands work with admin or owner only.__")
        return
    if not m.reply_to_message:
        await m.reply_text("❌ **Please reply to a message to forward broadcast!**")
        return
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            # print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(
        f"✅Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users."
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Restart ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("restart"))
async def restart_bot(_, m: Message):
    if not m.from_user or m.from_user.id != cfg.OWNER_ID:
        await m.reply_text("🔒 **Permission Denied**\n\n__Only the main bot owner can restart the bot!__")
        return
    await m.reply_text("🔄 **Restarting the bot... Please wait.**")
    os.execv(sys.executable, [sys.executable] + sys.argv)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Sudo Management ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("addsudo"))
async def addsudo_cmd(_, m: Message):
    if not m.from_user or m.from_user.id != cfg.OWNER_ID:
        await m.reply_text("🔒 **Permission Denied**\n\n__Only the main bot owner can manage sudo users!__")
        return

    user_id = None
    if m.reply_to_message:
        if m.reply_to_message.from_user:
            user_id = m.reply_to_message.from_user.id
    elif len(m.command) > 1:
        try:
            user_id = int(m.command[1])
        except ValueError:
            try:
                user = await app.get_users(m.command[1])
                user_id = user.id
            except Exception as e:
                await m.reply_text(f"❌ **Invalid User ID/Username:** {e}")
                return
    
    if not user_id:
        await m.reply_text("❌ **Please reply to a user's message or provide a User ID / Username!**\n\n**Usage:** `/addsudo [user_id/username]` or reply to a message with `/addsudo`.")
        return

    add_sudo(user_id)
    await m.reply_text(f"✅ **Successfully added user `{user_id}` to sudoers!**")


@app.on_message(filters.command(["delsudo", "removesudo"]))
async def delsudo_cmd(_, m: Message):
    if not m.from_user or m.from_user.id != cfg.OWNER_ID:
        await m.reply_text("🔒 **Permission Denied**\n\n__Only the main bot owner can manage sudo users!__")
        return

    user_id = None
    if m.reply_to_message:
        if m.reply_to_message.from_user:
            user_id = m.reply_to_message.from_user.id
    elif len(m.command) > 1:
        try:
            user_id = int(m.command[1])
        except ValueError:
            try:
                user = await app.get_users(m.command[1])
                user_id = user.id
            except Exception as e:
                await m.reply_text(f"❌ **Invalid User ID/Username:** {e}")
                return
    
    if not user_id:
        await m.reply_text("❌ **Please reply to a user's message or provide a User ID / Username!**\n\n**Usage:** `/delsudo [user_id/username]` or reply to a message with `/delsudo`.")
        return

    remove_sudo(user_id)
    await m.reply_text(f"🗑️ **Successfully removed user `{user_id}` from sudoers!**")


@app.on_message(filters.command(["sudolist", "sudoers"]))
async def sudolist_cmd(_, m: Message):
    if not m.from_user or m.from_user.id != cfg.OWNER_ID:
        await m.reply_text("🔒 **Permission Denied**\n\n__Only the main bot owner can view the sudo users list!__")
        return

    static_sudos = cfg.SUDO
    dynamic_sudos = get_sudolist()

    text = "👑 **RS Auto Approval Sudoers** 👑\n\n"
    
    owner_str = f"`{cfg.OWNER_ID}`"
    try:
        owner_user = await app.get_users(cfg.OWNER_ID)
        owner_str = f"{owner_user.mention} (`{cfg.OWNER_ID}`)"
    except Exception:
        pass
    text += f"👑 **Owner (Full Access):**\n{owner_str}\n\n"
    
    text += "👤 **Static Sudoers (Config):**\n"
    if static_sudos:
        for s in static_sudos:
            user_str = f"`{s}`"
            try:
                u = await app.get_users(s)
                user_str = f"{u.mention} (`{s}`)"
            except Exception:
                pass
            text += f"• {user_str}\n"
    else:
        text += "_None_\n"
        
    text += "\n⚙️ **Dynamic Sudoers (Database):**\n"
    if dynamic_sudos:
        for s in dynamic_sudos:
            user_str = f"`{s}`"
            try:
                u = await app.get_users(s)
                user_str = f"{u.mention} (`{s}`)"
            except Exception:
                pass
            text += f"• {user_str}\n"
    else:
        text += "_None_\n"

    text += "\n__Powered By : @rs_bro__"
    
    await m.reply_text(text)


logging.info("I'm Alive Now!")
app.run()
