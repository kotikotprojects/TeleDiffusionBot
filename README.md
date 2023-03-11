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

## Environment
```env
TOKEN=
ADMIN=
DB_CHAT=
DB_PATH=
ENCRYPTION_KEY=
```
Add these variables to `.env` file or set up environment key-value on your hosting

## Env keys and values:
They should be in `KEY='VALUE'` format
### TOKEN
Bot token from BotFather

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
to restore database. Path can be `.` to store in same folder

### ENCRYPTION_KEY
Password to encrypt some database fields. Do not share it.

## Starting bot
Type `/start` in new bot PM to set up everything. 

Install [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
and run it with `--api` argument (for me arguments are `--no-half --xformers --api`)

Run `/setendpoint http://endpoint_address:port`

Bot is ready to use!