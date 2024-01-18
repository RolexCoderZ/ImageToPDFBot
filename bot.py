# code dev by t.me/Mr_RoleXG
# © @Mr_RoleXG
# Use The Code With Credits To t.me/Mr_RoleXG otherwise Strict Action will be taken
import os
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from myrogram import notJoin, forceMe, STARTER, BOTBY

TOKEN = os.environ.get("TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

app = Client(
    "pdf",
    bot_token=TOKEN, api_hash=API_HASH,
    api_id=API_ID
)

print("Bot Started! © t.me/Mr_RoleXG")
LIST = {}

def is_user_joined_channel(client, user_id):
    try:
        user = client.get_chat_member("@ProCoderZ_Bots", user_id)
        return user.status != "kicked"
    except UserNotParticipant:
        return False

@app.on_message(filters.command(['start']))
def start(client, message):
    user_id = message.from_user.id
    res = forceMe(message.chat.id)

    if res == "no":
        return notJoin(client, message)

    # Check if the user is a member of the specified channel
    if not is_user_joined_channel(client, user_id):
        return message.reply_text("Hey 👋 Friend Please join our channel @ProCoderZ_Bots to use this bot. After Joining The Channel Click On /start To Use This Bot.")

    # User is a member, proceed with the bot's functionality
    message.reply_text(text=f"""Hello {message.from_user.first_name}, I am an image to pdf bot.

I can convert images to pdf.

**Send me images and at the end send /convert**

This bot was created by {BOTBY}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Updates Channel 🇮🇳", url=f"https://t.me/ProCoderZ_Bots")],
            [
                InlineKeyboardButton("Developer ⚡", url="https://t.me/Mr_RoleXG")]
        ]))

@app.on_message(filters.private & filters.photo)
async def pdf(client, message):
    if not isinstance(LIST.get(message.from_user.id), list):
        LIST[message.from_user.id] = []

    file_id = str(message.photo.file_id)
    ms = await message.reply_text("Converting To PDF Please Wait......")
    file = await client.download_media(file_id)

    image = Image.open(file)
    img = image.convert('RGB')
    LIST[message.from_user.id].append(img)
    await ms.edit(
        f"{len(LIST[message.from_user.id])} image   Successful Created PDF if you want add more image Send me One by one\n\n **if done click here 👉 /convert\n\nReport Errors Here @TeamCoderZ_Bot** ")

@app.on_message(filters.command(['convert']))
async def done(client, message):
    images = LIST.get(message.from_user.id)

    if isinstance(images, list):
        del LIST[message.from_user.id]
    if not images:
        await message.reply_text("No image Please Send Image First!!")
        return

    path = f"{message.from_user.id}" + ".pdf"
    images[0].save(path, save_all=True, append_images=images[1:])

    await client.send_document(message.from_user.id, open(path, "rb"), caption="Here is your pdf !! More Bots @ProCoderZ_Bots")
    os.remove(path)

app.run()
  
