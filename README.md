# Auto-Approve-Bot
👾 Hey I'll Accept telegram join requests. Easy to use and simple.

## 🚀 Demo Bot

<h2>〽️ Deploy Me </h2> 

<details><summary>📌 Deploy to VPS/Local </summary>


  ```ssh
  git clone https://github.com/ImDenuwan/Auto-Approve-Bot
  pip3 install -r requirements.txt
  # fill config.py vars
  python3 bot.py
  ```

</details>

## 🏷 Environment Variables
  - `API_ID` - Your Telegram API ID. Get it [Here](https://my.telegram.org)
  - `API_HASH` - Your Telegram API HASH. Get it [Here](https://my.telegram.org)
  - `MONGO_URI` - Add MongoDB Database URI.
  - `BOT_TOKEN` - Your Bot Token. Get it from [Here](https://t.me/BotFather)
  - `CHID` - Your Force subscribe channel id. Get it from @MissRose_Bot
  - `FSUB` - Force subscribe channel username without `@`
  - `OWNER_ID` - The Telegram ID of the primary/main bot owner (has full root access, restarts, sudoer management).
  - `SUDO` - Bot sudo user IDs (for statistics and broadcast access). Separate multiple IDs with spaces.
  
## 🤖 Bot Commands
### 👑 Owner Only
  - `/restart` - Restarts the bot's process.
  - `/addsudo <id/username>` - Promotes a user to Sudo. (Or reply to their message with `/addsudo`)
  - `/delsudo <id/username>` - Demotes a user from Sudo. (Or reply to their message with `/delsudo`)
  - `/sudolist` - Views all static and dynamic Sudo/Owner users.

### 👥 Sudo & Owner
  - `/start` - Starts the bot and provides information.
  - `/users` - Gets bot statistics (total users and groups).
  - `/bcast` - Broadcasts a message to all users. (Reply to a message with this command)
  - `/fcast` - Forward broadcasts a message to all users. (Reply to a message with this command)
  
### 💫 Credits
 - [Dan](https://github.com/delivrance) for Pyrogram
 - [Me](https://github.com/ImDenuwan) for Nothing 😅
