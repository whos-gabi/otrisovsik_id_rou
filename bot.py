from dotenv import load_dotenv
from fakedraw import printID
from main import generateUser

import aiogram
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import os


load_dotenv()
global id_path
# from main import generateID

# to update requirements.txt
# pipreqs . --force 

BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Start the bot"),
        types.BotCommand(command="/help", description="Get help"),
        types.BotCommand(command="/generate_id", description="Generate an ID")
    ]
    await bot.set_my_commands(commands)

async def on_startup(dp: Dispatcher):
    await set_commands(bot)



@dp.message_handler(commands=['start'])
async def handle_start(message):
    await bot.send_photo(message.chat.id, open("src/CI_logo.png", 'rb'))
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    reply_markup.add(types.KeyboardButton(text="/generate_id"), types.KeyboardButton(text="/help"))

    await bot.send_message(message.chat.id, "Hey, to generate an ID send me a message with text: /generate_id\nor click the button below.", reply_markup=reply_markup)
	
@dp.message_handler(commands=['help'])
async def handle_help(message):
    await bot.send_message(message.chat.id, "I am DocWriterRo, and I can help you generate an ID.\n You can use the following commands: \n/start \n/help \n/generate_id")
	

@dp.message_handler(commands=['generate_id'])
async def handle_generate_id(message):
    await bot.send_message(message.chat.id, "Generating ID 🪪⏳")

    user_data = await generateUser()
    id_path = await printID(user_data)

    if os.path.exists(id_path):
        try:
            with open(id_path, 'rb') as id_image:
                await message.answer_photo(id_image)
            with open(id_path, 'rb') as id_image:
                await message.answer_document(id_image)
        except Exception as e:
            await message.reply(f"Error: {e}")
        await bot.send_message(message.chat.id, "Done ✅")
        os.remove(id_path)
    else:
        await message.reply("Nu s-a putut genera buletinul de identitate.")



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)