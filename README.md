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
  - `API_ID` - Your Telegram API ID.Get it [Here](my.telegram.org)
  - `API_HASH` - Your Telegram API HASH.Get it [Here](my.telegram.org)
  - `MONGO_URI` - Add MongoDB Database URI.
  - `BOT_TOKEN` - Your Bot Token. Get it from [Here](https://t.me/BotFather)
  - `CHID` - Your Force subscribe channel id Get it from @MissRose_Bot
  - `FSUB` - Force subscribe channel username without `@`
  - `SUDO` - bot owners Id/ ids ( for broadcast and stats cmds). for multiple use space.
  
## 🤖 Bot Commands
  - `/start` - Starts the bot and provides information.
  - `/users` - (Sudo User Only) Get bot statistics (total users and groups).
  - `/bcast` - (Sudo User Only) Broadcast a message to all users. (Reply to a message with this command)
  - `/fcast` - (Sudo User Only) Forward a message to all users. (Reply to a message with this command)
  
### 💫 Credits
 - [Dan](https://github.com/delivrance) for pyrogram
 - [Me](https://github.com/ImDenuwan) for Nothing 😅
