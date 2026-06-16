from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    ChatMemberUpdated,
)
from pyrogram import filters, Client, errors, enums, idle
from pyrogram.errors import UserNotParticipant, ChannelPrivate, PeerIdInvalid
from pyrogram.errors.exceptions.flood_420 import FloodWait

# Monkey patch Client.get_messages to handle private channel replies gracefully
original_get_messages = Client.get_messages

async def patched_get_messages(self, *args, **kwargs):
    try:
        return await original_get_messages(self, *args, **kwargs)
    except (ChannelPrivate, PeerIdInvalid):
        return None

Client.get_messages = patched_get_messages
from database import (
    add_user,
    add_group,
    all_users,
    all_groups,
    users,
    groups,
    remove_user,
    add_sudo,
    remove_sudo,
    get_sudolist,
    get_all_groups_details,
)
from configs import cfg
import random, asyncio, os, sys, threading
from flask import Flask

flask_app = Flask(__name__)

@flask_app.route('/')
def hello_world():
    return 'I am Alive'

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

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

bot_id = None

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
        chat_type = "channel" if m.chat.type == enums.ChatType.CHANNEL else "group"
        add_group(m.chat.id, title=m.chat.title, username=m.chat.username, invite_link=m.chat.invite_link, chat_type=chat_type)
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


@app.on_chat_member_updated()
async def chat_member_handler(_, update: ChatMemberUpdated):
    global bot_id
    if not bot_id:
        return
        
    target_user = None
    if update.new_chat_member:
        target_user = update.new_chat_member.user
    elif update.old_chat_member:
        target_user = update.old_chat_member.user
        
    if target_user and target_user.id == bot_id:
        status = update.new_chat_member.status if update.new_chat_member else None
        if status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.MEMBER]:
            chat = update.chat
            chat_type = "channel" if chat.type == enums.ChatType.CHANNEL else "group"
            add_group(
                chat.id,
                title=chat.title,
                username=chat.username,
                invite_link=chat.invite_link,
                chat_type=chat_type
            )
        elif status in [enums.ChatMemberStatus.BANNED, enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.RESTRICTED] or not status:
            try:
                groups.delete_one({"chat_id": str(update.chat.id)})
            except Exception:
                pass


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
            chat_type = "channel" if m.chat.type == enums.ChatType.CHANNEL else "group"
            add_group(m.chat.id, title=m.chat.title, username=m.chat.username, invite_link=m.chat.invite_link, chat_type=chat_type)
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

async def get_page_groups(client, page=1, page_size=5):
    all_grps = get_all_groups_details()
    if not all_grps:
        return "❌ **No groups or channels are currently registered in the database.**", None
        
    # Dynamic deduplication and automatic background database cleanup
    seen_ids = set()
    unique_grps = []
    for g in all_grps:
        chat_id = g.get("chat_id")
        if not chat_id:
            continue
        if chat_id in seen_ids:
            try:
                groups.delete_one({"_id": g["_id"]})
            except Exception:
                pass
            continue
        seen_ids.add(chat_id)
        unique_grps.append(g)
        
    active_grps = []
    for g in unique_grps:
        chat_id = g.get("chat_id")
        title = g.get("title")
        username = g.get("username")
        invite_link = g.get("invite_link")
        chat_type = g.get("chat_type")
        first_failed_at = g.get("first_failed_at")
        
        is_accessible = True
        try:
            chat = await client.get_chat(int(chat_id))
            title = chat.title or title
            username = chat.username or username
            invite_link = chat.invite_link or invite_link
            chat_type = "channel" if chat.type == enums.ChatType.CHANNEL else "group"
            add_group(chat_id, title=title, username=username, invite_link=invite_link, chat_type=chat_type, unset_failed=True)
        except FloodWait:
            pass
        except Exception:
            from datetime import datetime
            # Track failure timestamp in MongoDB to prevent accidental restart deletion
            if not first_failed_at:
                first_failed_at = datetime.utcnow()
                add_group(chat_id, first_failed_at=first_failed_at)
                
            # If it has been failing for more than 7 days, delete from database
            if (datetime.utcnow() - first_failed_at).days >= 7:
                try:
                    groups.delete_one({"chat_id": str(chat_id)})
                except Exception:
                    pass
                is_accessible = False
            
        if is_accessible:
            active_grps.append({
                "chat_id": chat_id,
                "title": title,
                "username": username,
                "invite_link": invite_link,
                "chat_type": chat_type
            })
            
    total_chats = len(active_grps)
    if total_chats == 0:
        return "❌ **No active groups or channels are currently registered/accessible.**", None
        
    total_pages = (total_chats + page_size - 1) // page_size
    
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages
        
    start = (page - 1) * page_size
    end = start + page_size
    page_items = active_grps[start:end]
    
    text = "👥 **RS Auto Approval Chat Directory** 👥\n\n"
    count = start + 1
    
    for g in page_items:
        chat_id = g.get("chat_id")
        title_str = g.get("title") or "Unknown Chat"
        username = g.get("username")
        invite_link = g.get("invite_link")
        chat_type = g.get("chat_type")
        
        id_str = f"`{chat_id}`"
        
        if username:
            usr_str = f"@{username}"
            link_str = f"[Click Here](https://t.me/{username})"
        else:
            usr_str = "_Private Chat_"
            if invite_link:
                link_str = f"[Invite Link]({invite_link})"
            else:
                link_str = "_No Link Available_"
                
        type_label = "📣 **Channel:**" if chat_type == "channel" else "👥 **Group:**"
        text += f"{count}. {type_label} {title_str}\n"
        text += f"   🆔 **ID:** {id_str}\n"
        text += f"   🌐 **Username:** {usr_str}\n"
        text += f"   🔗 **Link:** {link_str}\n\n"
        count += 1
        
    text += f"📊 **Page:** `{page}` / `{total_pages}` | **Total Chats:** `{total_chats}`\n\n__Powered By : @rs_bro__"
    
    # Generate Keyboard buttons for pagination
    buttons = []
    row = []
    if page > 1:
        row.append(InlineKeyboardButton("◀️ Previous", callback_data=f"groups_page_{page-1}"))
    if page < total_pages:
        row.append(InlineKeyboardButton("Next ▶️", callback_data=f"groups_page_{page+1}"))
        
    if row:
        buttons.append(row)
    buttons.append([InlineKeyboardButton("🔙 Back to Stats", callback_data="back_stats")])
    
    keyboard = InlineKeyboardMarkup(buttons)
    return text, keyboard


@app.on_message(filters.command("users"))
async def dbtool(_, m: Message):
    if not m.from_user or not is_sudo(m.from_user.id):
        await m.reply_text("🔒 **Permission Denied**\n\n__You are not an admin! These commands work with admin or owner only.__")
        return
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    
    keyboard = None
    if m.from_user.id == cfg.OWNER_ID:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 View Groups", callback_data="view_groups"
                    )
                ]
            ]
        )
    
    await m.reply_text(
        text=f"""📊 **RS Auto Approval Stats** 📊

┌──🙋‍♂️ **Total Users:** `{xx}`
├──👥 **Total Groups:** `{x}`
└──🚧 **Grand Total:** `{tot}`

__Powered By : @rs_bro__""",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("^view_groups$|^groups_page_"))
async def cb_view_groups(_, cb: CallbackQuery):
    if not cb.from_user or cb.from_user.id != cfg.OWNER_ID:
        await cb.answer("🔒 Permission Denied: Main owner only!", show_alert=True)
        return
        
    page = 1
    if cb.data.startswith("groups_page_"):
        try:
            page = int(cb.data.split("_")[-1])
        except Exception:
            page = 1
            
    await cb.answer("Loading chat directory...")
    try:
        report, markup = await get_page_groups(app, page=page)
        await cb.message.edit(report, reply_markup=markup, disable_web_page_preview=True)
    except Exception as e:
        logging.error(f"Error in view_groups callback: {e}")
        await cb.message.edit(f"❌ **An error occurred:** {e}")


@app.on_callback_query(filters.regex("back_stats"))
async def cb_back_stats(_, cb: CallbackQuery):
    if not cb.from_user or not is_sudo(cb.from_user.id):
        await cb.answer("🔒 Permission Denied: Sudoers only!", show_alert=True)
        return
        
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    
    keyboard = None
    if cb.from_user.id == cfg.OWNER_ID:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 View Groups", callback_data="view_groups"
                    )
                ]
            ]
        )
    
    await cb.message.edit(
        text=f"""📊 **RS Auto Approval Stats** 📊

┌──🙋‍♂️ **Total Users:** `{xx}`
├──👥 **Total Groups:** `{x}`
└──🚧 **Grand Total:** `{tot}`

__Powered By : @rs_bro__""",
        reply_markup=keyboard
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

    total = success + failed + blocked + deactivated
    await lel.edit(
        f"""📢 **RS Broadcast Campaign Completed** 📢

┌── ✅ **Success:** `{success}` users
├── ❌ **Failed:** `{failed}` users
├── 👾 **Blocked:** `{blocked}` users
└── 👻 **Deactivated:** `{deactivated}` users

📈 **Total Reached:** `{success}` / `{total}` users

__Powered By : @rs_bro__"""
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

    total = success + failed + blocked + deactivated
    await lel.edit(
        f"""📢 **RS Broadcast Campaign Completed** 📢

┌── ✅ **Success:** `{success}` users
├── ❌ **Failed:** `{failed}` users
├── 👾 **Blocked:** `{blocked}` users
└── 👻 **Deactivated:** `{deactivated}` users

📈 **Total Reached:** `{success}` / `{total}` users

__Powered By : @rs_bro__"""
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Restart ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("restart"))
async def restart_bot(_, m: Message):
    if not m.from_user or m.from_user.id != cfg.OWNER_ID:
        await m.reply_text("🔒 **Permission Denied**\n\n__Only the main bot owner can restart the bot!__")
        return
    
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Yes", callback_data="confirm_restart"),
                InlineKeyboardButton("❌ No", callback_data="cancel_restart")
            ]
        ]
    )
    await m.reply_text(
        "⚠️ **Are you sure you want to restart the bot?**\n\n_Accidental restarts can interrupt active processes._",
        reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("confirm_restart"))
async def cb_confirm_restart(_, cb: CallbackQuery):
    if not cb.from_user or cb.from_user.id != cfg.OWNER_ID:
        await cb.answer("🔒 Permission Denied: Main owner only!", show_alert=True)
        return
    await cb.message.edit("🔄 **Restarting the bot... Please wait.**")
    try:
        with open("restart.txt", "w") as f:
            f.write(f"{cb.message.chat.id}\n{cb.message.id}")
    except Exception as e:
        logging.error(f"Failed to write restart file: {e}")
    os.execv(sys.executable, [sys.executable] + sys.argv)


@app.on_callback_query(filters.regex("cancel_restart"))
async def cb_cancel_restart(_, cb: CallbackQuery):
    if not cb.from_user or cb.from_user.id != cfg.OWNER_ID:
        await cb.answer("🔒 Permission Denied: Main owner only!", show_alert=True)
        return
    await cb.message.edit("❌ **Restart cancelled!**")


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


async def main():
    global bot_id
    # Start the Flask web server in a background thread to satisfy Dokploy's health checks
    threading.Thread(target=run_flask, daemon=True).start()
    
    # 15 seconds startup delay to prevent multi-instance conflicts during rolling deployments
    logging.info("Delaying startup by 15 seconds to prevent multi-instance conflicts...")
    await asyncio.sleep(15)
    
    await app.start()
    logging.info("I'm Alive Now!")
    
    try:
        me = await app.get_me()
        bot_id = me.id
    except Exception as e:
        logging.error(f"Failed to fetch bot info: {e}")
    
    if os.path.exists("restart.txt"):
        try:
            with open("restart.txt", "r") as f:
                lines = f.read().splitlines()
            if len(lines) >= 2:
                chat_id = int(lines[0])
                msg_id = int(lines[1])
                await app.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_id,
                    text="✅ **Bot restarted successfully!**"
                )
        except Exception as e:
            logging.error(f"Failed to update restart message: {e}")
        finally:
            try:
                os.remove("restart.txt")
            except Exception:
                pass
                
    await idle()
    await app.stop()


if __name__ == "__main__":
    app.run(main())
