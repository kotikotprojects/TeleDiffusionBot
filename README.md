# Bars's TeleDiffusionBot
Open-source Telegram bot based on aiogram that uses
[AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
as backend. 

# Features:
- Database hosting in telegram
- Prompts, negative prompts, multi models support and many other features from webui
- Saving and restoring prompts from pictures
- Many admins for bot
- Easy-to-edit code
- Bot hosting and StableDiffusion hosting can be separate

# Screenshots
![generated](https://i.imgur.com/1Lm2T2v.png)
![config](https://i.imgur.com/LhqKMAH.png)

...try it yourself!

# Setup instructions
### If using replit:
```commandline
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Env variables setup is completed by adding them in menu (environment setup is described later)

### If using other hosting:
Setup bot as usually, environment setup is described later

### If hosting locally:
Create `.env` file in root of bot directory

### Important
Remember to run `/start` command in bot from admin account to set everything up after filling environment and running it.

## Environment
```env
TOKEN=
ADMIN=
DB_CHAT=
DB_PATH=
ENCRYPTION_KEY=
ARCHIVE_CHAT=
```
Add these variables to `.env` file or set up environment key-value on your hosting

## Env keys and values:
They should be in `KEY='VALUE'` format
### TOKEN
Bot token from BotFather

Bot `privacy` should be disabled.
```
Sequence within a BotFather chat:
You: /setprivacy
BotFather: Choose a bot to change group messages settings.
You: @your_name_bot
BotFather: 'Enable' - your bot will only receive messages that either start with the '/' symbol or mention the bot by username.
'Disable' - your bot will receive all messages that people send to groups.
Current status is: ENABLED
You: Disable
BotFather: Success! The new status is: DISABLED. /help
```
[Source](https://stackoverflow.com/questions/38565952/how-to-receive-messages-in-group-chats-using-telegram-bot-api)

### ADMIN
Your id. To get it, use [@userinfobot](https://t.me/userinfobot). Send any message to this bot and copy your id.

### DB_CHAT
This is needed to host database in telegram. Create new group or use old group with databases.
Invite @RawDataBot to your group:

![](https://i.imgur.com/7qs9QRT.png)

Find this string and kick bot:

![](https://i.imgur.com/6BYwbkN.png)

Add value to `DB_CHAT` variable. For me it is `-816497374`

### DB_PATH
Path to folder where `db` and `dbmeta` are stored. `dbmeta` is file, that you need to copy when moving to other hosting
to restore database. Path can be `.` to store in same folder. For me now it is `/home/barstiger/db/TeleDiffusionBot`

### ENCRYPTION_KEY
Password to encrypt some database fields. Do not share it.

### ARCHIVE_CHAT
Images, generated using bot will be sent to this group by id. Bot should be added to group. This is optional.

## Starting bot
Type `/start` in new bot PM to set up everything. 

If you see errors or warnings (such as `🔄️ Bot database synchronised because of restart. 
If you tried to run a command, run it again`), run `/start` command again and again until you
will receive expected output (some messages with `👋 Hello, YOUR NAME....` and `✅` boxes). It is needed to 
mark up database and create all tables, restart bot and sync database.

After that, install [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
and run it with `--api` argument (for me arguments are `--no-half --xformers --api --listen` to properly work with newer SD models and work in local network). 
Make sure that `Add model name to generation information` is enabled in settings!

![](https://user-images.githubusercontent.com/16289552/225164914-8423cab7-6b85-42e8-b799-c89bfe8b7692.png)

Run `/setendpoint http://endpoint_address:port`. For me now it is `http://192.168.50.30:7860`, WITHOUT BACKSLASH at the end

Bot is ready to use!

### If something doesnt work, check subsequence of actions:

- clone repo
- cd to repo
- create python venv
- install requirements
- create `.env` file and fill it
- run `python main.py`
- `/start` 2-3 times to bot private messages (until you see expected output)
- `/setendpoint` command with proper args
