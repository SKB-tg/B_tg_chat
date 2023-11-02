"""Сервер Telegram бота, запускаемый непосредственно"""
from  app.g4f_last import OpenaiFreeLast 
import time
import asyncio
from asyncio import Lock
import logging
import os
from typing import Any, Dict
from dotenv import load_dotenv

#import aiohttp
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request

from aiogram import Bot, Dispatcher, types, F, Router, html # executor,
#from aiogram.utils.executor import start_polling, start_webhook
from aiogram.filters import Command, Filter, StateFilter
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, Message, MenuButtonWebApp, WebAppInfo, Update
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardBuilder
from aiogram.handlers import CallbackQueryHandler
from app.models import add_tg_user, tg_user_is_db, get_tguser, TgUser, update_coloms_user, tguser
# import inc.db
# import inc.exceptions
# import inc.expenses
# from inc.categories import Categories
# from inc.middlewares import AccessMiddleware

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY_API = os.getenv("OPENAI_KEY_API")
#print(OPENAI_KEY_API, TELEGRAM_BOT_TOKEN_2)

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
    new_user=TgUser(**{})
    new_user.codename=user.username
    new_user.id_chat=user.id
    new_user.first_name=user.first_name
    new_user.is_bot=user.is_bot
    new_user.is_donate=False
    new_user_str = str(new_user)
    #new_user_str.replace(" ", "")
    #Запрос в ДБ и отсылка тг
    requests.get(f'https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id=5146071572&text={new_user_str}')
    return new_user

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
async def command_start(message: Message, state: FSMContext, bot: Bot, base_url: str) -> None:
    #await state.set_state(Form.name)
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Разбуди бота", web_app=WebAppInfo(url=f"{base_url}")),# "Меню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\nМеню\n/newpost     Создать новы пост\n/newdraft     Создать черновой пост\n/newpost     Создать новы пост\n/newpost     Создать новы пост\n/newpost     Создать  новы пост\n"
    )
    user_name= message.from_user.username
    if tg_user_is_db(user_name) == False:
        print(82)
        _new_user={}
        _new_user['codename']=message.from_user.username
        _new_user['id_chat']=message.from_user.id
        _new_user['last_name']=message.from_user.last_name
        _new_user['first_name']=message.from_user.first_name
        _new_user['is_bot']=message.from_user.is_bot
        _new_user['is_donate']=False

        add_tg_user(_new_user)
        await save_newuser(message.from_user)
    await message.answer(
        'Hello friend! Ты попал в приватный чат для общения и консультаций !\nЕсли у вас нет промокода\n("/promo-****" * - символ) Войти по промокоду\n"/donate" Войти с переводом доната\n"/help" справочная информация по HelperGPT\nВведите и отправте /promo и 4-ре символа промокода(прим.- /promo-555m)\nили отправте команду-/donate',
         reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Command(commands=["help"]))
async def command_help(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    await message.answer(
        "Hello friend! Ты попал в чат для общения и консультаций(на алгоритме типа ИИ)\nИзвините раздел в разработке",

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
        "Добро пожаловать, у вас полный доступ к действующему функционалу\nЗадавайте вопросы, делитесь мнениями...",

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

@form_router.message( F.chat.func(lambda chat: chat.type == 'private'))
async def process_write_menu2_bots(message: types.Message) -> None:
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    print(121, message.chat.type, get_tguser(user_name).codename )
    # if tg_user_is_db(user_name) != False:
    #     await save_newuser(message.from_user)
    _is_donat=get_tguser(user_name).is_donate
    if ((message.text == '/promo') or (_is_donat == False)) :
        await message.answer(
            "Неправильно набрана команда, повторите!",
            reply_markup=ReplyKeyboardRemove())
        return
    else:
        # Получаем и обрабатываем сообщение 
        response = OpenaiFreeLast.get_answer_ofl(message.text, first_name=first_name)
        answer=response # 'Ответ HelperGPT:\n' + response['choices'][0]['text']

        await message.answer(
            answer,
                reply_markup=ReplyKeyboardRemove())

@form_router.message( F.chat.func(lambda chat: chat.type == 'supergroup'))
async def process_talk_bots(message: types.Message) -> None:
    # await state.clear()
    # await state.set_state(Form.menu)
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    if tg_user_is_db(user_name) == False:
        new_user_dict = dict(await save_newuser(message.from_user))
        add_tg_user(new_user_dict)
    print(177, message.chat.type )

    # Получаем и обрабатываем сообщение 
    response = OpenaiFreeLast.get_answer_ofl(message.text, first_name=first_name)
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
        return
        async with timeout(15) as cm:
            await requests.get('https://desing-profi.onrender.com')
        if cm.expired == True:
            return
    except asyncio.TimeoutError as e:
        print(e)
        return
    finally:
        return

from pathlib import Path

async def demo_handler(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "app/index.html")
    print(Path(__file__).parent.resolve())

async def on_startup(bot: Bot, base_url: str):
    await bot.delete_webhook()
    await bot.set_webhook(f"{base_url}/webhook")


def main():
    # form_router = Router()
    # dp = Dispatcher()
    dp.include_router(form_router)

    app = Application()
    dp["base_url"] = base_url
    app["bot"] = bot
    dp.startup.register(on_startup)

    #await dp.start_polling(bot)
    #update = Update.model_validate(await request.json(), context={"bot": bot})
    #useful_updates = dp.resolve_used_update_types()

    #dp.feed_update(bot=bot, update=incoming_update)
    #await on_startup(bot, base_url)
    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    SimpleRequestHandler(
        dispatcher=dp, bot=bot,
    ).register(app, path="/webhook")
    app.router.add_get("/", demo_handler)
    setup_application(app, dp, bot=bot)

    run_app(app, host="0.0.0.0", port=80)

if __name__ == '__main__':
    main()


