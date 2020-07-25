from telethon.sync import TelegramClient
from telethon import functions
from telethon import types as teletypes
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from os import getenv

load_dotenv(verbose=True)
logging.basicConfig(level=logging.INFO)

name = getenv('USER_NAME')
number = getenv('PHONE_NUMBER')
api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
channel = getenv('CHANNEL')
channel_id = getenv('CHANNEL_ID')
bot_token = getenv('BOT_TOKEN')

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


async def get_users():
    users_string = ''
    async with TelegramClient(name, api_id, api_hash) as client:

        me = await client.get_me()
        print(me.username)

        try:
            result = await client(functions.channels.GetParticipantsRequest(
                channel=channel_id,
                filter=teletypes.ChannelParticipantsRecent(),
                offset=0,
                limit=100,
                hash=0
            ))

        #    print(result.stringify())

            for user in result.users:
                print(user.id, user.username, user.first_name, user.last_name)
                users_string += str(user.id) + ' ' + user.username + ' ' + user.first_name 
                if user.last_name:
                    users_string += ' ' + str(user.last_name) + "\n"
                else:
                    users_string += "\n"
        except ValueError as e:
            users_string = e
    return users_string


@dp.message_handler()
async def get_messages(msg: types.Message):
    reply = ''
    if msg.text == '/show_users':
        reply = await get_users()
    elif msg.text == "/help":
        reply = "Команды: \n /show_users - посмотреть юзеров"
    else:
        reply = "Левая команда. Напиши /help."
    await msg.reply(reply)

executor.start_polling(dp, skip_updates=True)
