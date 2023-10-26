"""Сервер Telegram бота, запускаемый непосредственно"""
from  app.g4f_last import OpenaiFreeLast 
import time
import asyncio
from asyncio import Lock
import logging
import os
from typing import Any, Dict
from dotenv import load_dotenv

import aiohttp
from aiogram import Bot, Dispatcher, types, F, Router, html # executor,
#from aiogram.utils.executor import start_polling, start_webhook
from aiogram.filters import Command, Filter, StateFilter
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, Message, MenuButtonWebApp, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardBuilder
from aiogram.handlers import CallbackQueryHandler
from app.models import add_tg_user, tg_user_is_db, get_tguser, TgUser, update_coloms_user
# import inc.db
# import inc.exceptions
# import inc.expenses
# from inc.categories import Categories
# from inc.middlewares import AccessMiddleware

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY_API = os.getenv("OPENAI_KEY_API")
print(OPENAI_KEY_API, TELEGRAM_BOT_TOKEN)

#lobal is_donat
is_donat = False
promokod = '1003'
promo="promo" + '-' + promokod

# Устанавливаем соединение с Telegram API 
bot = Bot(TELEGRAM_BOT_TOKEN)#'6334654557:AAE9uBbMvWfTAP6N4L57VIdX38ZLFPQZ9FM') 
base_url="https://b-tg-chat.onrender.com"

# Устанавливаем соединение с OpenAI API 
# openai.api_key = "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"
form_router = Router()
dp = Dispatcher()
dp.include_router(form_router)
#form_router.message.middleware(AccessMiddleware(ACCESS_ID))
#dp.middleware.setup(AccessMiddleware(ACCESS_ID))

class Form(StatesGroup):
    menu = State()
    submenu = State()
    submenu1 = State()
    submenu2 = State()
    name = State()
    like_bots = State()
    language = State()

#/**********************
async def save_newuser(user):
    new_user={}
    new_user['codename']=user.username
    new_user['id_chat']=user.id
    new_user['last_name']=user.last_name
    new_user['first_name']=user.first_name
    new_user['is_bot']=user.is_bot
    new_user['is_donate']=False
    
#***********************BOT-CHATBOT

# @form_router.message(Command(commands=["start"]))
# async def process_name(message: Message, state: FSMContext) -> None:
#     await message.answer(
#         f"Приветствую тебя,\nхочешь попробовать чатбот или бот-меню\nнажми на клаву?",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[[KeyboardButton(text="Чатбот"), KeyboardButton(text="Бот-меню")]],
#             resize_keyboard=True,)
#    )

    # @bot.message_handler(commands=["start"])
    # def start_message(message):
    #     bot.send_message(message.chat.id, 'Hello friend! Ты попал в чат HelperGPT(на алгоритме типа ИИ) для общения и консультаций принадлежащий закрытому сообществу!\nВход платный если у вас нет промокода\n("/promo-****" * - символ) Войти по промокоду\n"/donate" Войти с переводом доната\n"/help" справочная информация по HelperGPT\nВведите и отправте /promo и 4-ре символа промокода(прим.- /promo-555m)\nили отправте команду-/donate') # Настраиваем обработчики сообщений 


#@form_router.message(F.text.casefold() == "чатбот")
@form_router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Разбуди бота", web_app=WebAppInfo(url=f"{base_url}")),# "Меню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\nМеню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\n"
    )
    user_name= message.from_user.username
    if tg_user_is_db(user_name) == False:
        print(82)
        new_user={}
        new_user['codename']=message.from_user.username
        new_user['id_chat']=message.from_user.id
        new_user['last_name']=message.from_user.last_name
        new_user['first_name']=message.from_user.first_name
        new_user['is_bot']=message.from_user.is_bot
        new_user['is_donate']=False

        add_tg_user(new_user)
    await message.answer(
        'Hello friend! Ты попал в приватный чат для общения и консультаций !\nЕсли у вас нет промокода\n("/promo-****" * - символ) Войти по промокоду\n"/donate" Войти с переводом доната\n"/help" справочная информация по HelperGPT\nВведите и отправте /promo и 4-ре символа промокода(прим.- /promo-555m)\nили отправте команду-/donate',
         reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command(commands=["help"]))
async def command_help(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    await message.answer(
        "Hello friend! Ты попал в чат HelperGPT(на алгоритме типа ИИ)\nИзвините раздел в разработке",

        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Command(commands=[promo]))
async def command_promo(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    user_name= message.from_user.username
    # if get_tguser(user_name).is_donate != None:
    #     await message.answer(
    #         "Неправильно набран код, повторите!",
    #         reply_markup=ReplyKeyboardRemove())
    #     return
    id_db=get_tguser(user_name).id
    is_donate = True
    update_coloms_user(id_db, [{"is_donate": True},])
    await message.answer(
        "Добро пожаловать, у вас полный доступ к возможностям HelperGPT!\nЧем я могу Вам помочь?",

        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Command(commands=["donate"]))
async def command_donate(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
   #global is_donat
    #is_donat = True
    await message.answer(
        "Приветствем вас, ждите перевода на страницу оплаты...",

        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message( F.text != '🐊Наша экспертность')
async def process_write_menu2_bots(message: types.Message) -> None:
    # await state.clear()
    # await state.set_state(Form.menu)
    user_name = message.from_user.username
    #print(121, message.from_user.username, get_tguser(user_name).is_donate, TgUser.id)
    if tg_user_is_db(user_name) != False:
        save_newuser(message.from_user)
    _is_donat=TgUser.is_donate
    if (message.text == '/promo' or _is_donat == False) :
        print(_is_donat)
        await message.answer(
            "Неправильно набрана команда, повторите!",
            reply_markup=ReplyKeyboardRemove())
        return
    else:
        # Получаем и обрабатываем сообщение 
        response = OpenaiFreeLast.get_answer_ofl(message.text)
        # response = openai.Completion.create( 
        #     model="text-davinci-003", 
        #     prompt=message.text, 
        #     max_tokens=528, 
        #     temperature=0.7,
        #     top_p=1.0,
        #     frequency_penalty=0.2,
        #     presence_penalty=0.0, 
            #stop=["\n"] 
        #)
        answer=response # 'Ответ HelperGPT:\n' + response['choices'][0]['text']

        await message.answer(
            answer,
                reply_markup=ReplyKeyboardRemove())



#**************************END
#import async_timeout
from async_timeout import timeout
import time
import requests

async def consumer():
    print('Consumed start', 555+1)
    #Запрос в ДБ и отсылка тг
    #Запрос  на разбудить
    #requests.get('https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id=5146071572&text=start')
    time.sleep(1)
    try:
        async with timeout(30) as cm:
            await requests.get('https://desing-profi.onrender.com')
        print(cm.expired)
        if cm.expired == True:
            print(cm.expired)
            return
    except asyncio.TimeoutError as e:
        print(e)
        return
    finally:
        return


async def main():
    #requests.get('https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id='+str(5146071572)+'&text=start.')

    while True:
        try:
            async with timeout(610):
                await dp.start_polling(bot)

        except asyncio.TimeoutError as e:
           await consumer()



if __name__ == '__main__':
     asyncio.run(main())

#121 {'message_id': 3323, 'date': datetime.datetime(2023, 1, 29, 19, 53, 58, tzinfo=datetime.timezone.utc), 'chat': Chat(id=5146071572, type='private', title=None, username='kirill7979', first_name='Kirill 7979', last_name=None, photo=None,bio=None, has_private_forwards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None, description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_protected_content=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, location=None), 'from_user': User(id=5146071572, is_bot=False, first_name='Kirill 7979', last_name=None, username='kirill7979', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None), 'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': None, 'text': '/promo', 'entities': [MessageEntity(type='bot_command', offset=0, length=6, url=None, user=None, language=None, custom_emoji_id=None)], 'animation': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'caption_entities': None, 'contact': None, 'dice': None, 'game': None, 'poll': None, 'venue': None, 'location': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'message_auto_delete_timer_changed': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'passport_data': None, 'proximity_alert_triggered': None, 'video_chat_scheduled': None, 'video_chat_started': None, 'video_chat_ended': None, 'video_chat_participants_invited': None, 'web_app_data': None, 'reply_markup': None}