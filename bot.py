from aiogram import Dispatcher, Bot, executor, types 
import asyncio
import time
from aiogram.utils.markdown import hlink

token = '1778286965:AAHVRFvP7VK7YSvxj6ZXBFfaGPoXyI5sD5g'

bot = Bot(token)
dp = Dispatcher(bot)


async def send_mess(post):
    print(post)
    text = ''
    text += f'Название {post.post_title} \n'
    text += f'Стоимость {post.coast} \n'
    owner_href = hlink("Ссылка", post.owner_href)
    text += f'Ссылка на профиль арендодателя: {owner_href} \n'
    text += f'Номер арендодателя: {post.phone} \n'
    post_link = hlink('Ссыллка', post.post_url)
    text += f'Ссылка на объявление: {post_link} \n'
    for metro in post.metros:
        text += f'{metro.text} \n'
    print(text)
    await bot.send_message(chat_id=331579779, text=text, parse_mode='HTML')
    await bot.send_message(chat_id=847412749, text=text, parse_mode='HTML')

#async def main():
#    while True:
#        await send_mess('a')
#        time.sleep(100)


#asyncio.run(main())

