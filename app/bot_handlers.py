"""Сервер Telegram бота, запускаемый непосредственно"""
from  .g4f_last import OpenaiFreeLast 
import time
from async_timeout import timeout
import time
import requests
import json
import asyncio
from asyncio import Lock
import logging
import os
from typing import Any, Dict
from dotenv import load_dotenv
import random
#import aiohttp
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request

from aiogram import Bot, Dispatcher, types, F, Router, html # executor,
#from aiogram.utils.executor import start_polling, start_webhook
from aiogram.filters import Command, Filter, StateFilter, BaseFilter
from aiogram.enums import ParseMode
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, MessageEntity,
 InlineKeyboardButton, Message, MenuButtonWebApp, WebAppInfo, Update, Poll, PollAnswer, BufferedInputFile, FSInputFile, URLInputFile)
from aiogram.methods import GetMyCommands, DeleteMessage, GetChat

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, KeyboardBuilder
from aiogram.handlers import CallbackQueryHandler
from app.models import add_tg_user, tg_user_is_db, get_tguser, update_coloms_user, load_users, TgUser
from app.poll_handler import handle_correct_answer, p_router, QuizAnswer

from app.keyboard_button import get_inline_keyboard_creat, get_reply_keyboard2, get_reply_keyboard0, get_reply_keyboard4, get_reply_keyboard1, MyCallback, cb360, cb720, audio
from app.tube_pars import MyUniTuber
from app.u_utils import str_for_dict
#from app.bot_utils import get_message_id_by_keyword

from app.txt import txt
builder = InlineKeyboardBuilder()

#************************************

load_dotenv()
logging.basicConfig(level=logging.INFO)
BASE_URL = os.getenv("BASE_URL")
PORT = os.getenv("PORT")
FINISH_NUMBER = os.getenv("FINISH_NUMBER")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY_API = os.getenv("OPENAI_KEY_API")
#print(OPENAI_KEY_API, TELEGRAM_BOT_TOKEN_2)
ngrok = os.getenv("NGROK")


#lobal is_donat
is_donat = False
promokod = '1003'
promo="promo" + '-' + promokod

base_url = BASE_URL

# Устанавливаем соединение с Telegram API 
bot = Bot(TELEGRAM_BOT_TOKEN) 
# Устанавливаем соединение с OpenAI API 
# openai.api_key = "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"
cal_router = Router()
form_router = Router()
#dp = Dispatcher()
#form_router.message.middleware(AccessMiddleware(ACCESS_ID))
#dp.middleware.setup(AccessMiddleware(ACCESS_ID))
class GetAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.startswith(str(nomAdmin.u)) == True:
            return True
        return False


#****************************************************
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
#**********************************************
# @p_router.poll()
# async def poll_handler(poll: types.Poll):
#     mess=str(f"id:{poll.id} anan:{poll.is_anonymous}")
#     requests.get(f'https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id=5146071572&text={mess}')
 
 #*******************************************

#@form_router.message(F.text.casefold() == "чатбот")
@form_router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext, bot: Bot, base_url=base_url) -> None:
    #await state.set_state(Form.name)
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Глав. страница", web_app=WebAppInfo(url=f"{base_url}")),
    )
    # _command1: BotCommand = None
    _commands1: list = []
    _commands1 = [
    {"command": "help", "description": "помощь"},
    {"command": "start", "description": "рестарт"},
    {"command": "promo", "description": "ввести промо код"},
    {"command": "info_gid", "description": "справочная информация"},
    {"command": "settings", "description": "настройки бота"},
    {"command": "get_admin", "description": "Написать админу"},

    ]
    await bot.set_my_commands(_commands1)

    await state.storage.set_data('TgUser', {'donate': False})
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

        # list_tguser_username = load_users()
        # requests.get(f'https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id=5146071572&text={new_user_str}')

        add_tg_user(_new_user)
        await save_newuser(message.from_user)

    if get_tguser(user_name).is_donate:
        await state.storage.set_data('TgUser', {'donate': True})

    await message.answer(
        'Hello friend! Ты попал в приватный чат для общения и консультаций !\n\n---- BETTA-Version ----\n\nЯ использую разные языковые модели на основе ИИ.\nВыполняю функции администратора каналов, групповых чатов....\n Возможности постоянно обновляются.\nЕсли у вас нет промокода,\n а ведь я фанат экосистемы TON,\nты можешь пополнить мою коллекцию на 1TON.\n(для этого нажми на кн. "Глав. страница" - появятся пояснения)\n\nВведите и отправте /promo и 4-ре символа промокода(наприм.- /promo-555m)\n\n/help справочная информацияnn\n\n_--_',
         reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(txt.txt_vakancy, reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))
    #Заранее разбудим ресурс по вакансиям
    _url = "https://fastapi-pgstarterkit-test.onrender.com/status"
    res = requests.get(_url)
    print(res)


@form_router.message(Command(commands=["info_gid"]))
async def command_help_info(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)

    await message.answer(
        **txt.txt_info_gid.as_kwargs(),
        reply_markup=get_reply_keyboard1(),
    )

@form_router.message(Command("help"))
async def command_help(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    #result = await bot(GetMyCommands())
    await message.answer(**txt.txt_help.as_kwargs(),
        reply_markup=get_reply_keyboard1())

nomAdmin = MyCallback()

@form_router.message(Command(commands=["get_admin"]))
async def command_admin(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    nomAdmin.foo="bd"
    nomAdmin.u = random.randint(10000, 100000)
    ch = await state.get_data()
    chat_id_privat = 6034643381
    if ch["CH_ID"] == 5146071572:
           
        builder.add(
        types.InlineKeyboardButton(
        text="Оповещение",
        url=f'https://api.telegram.org/bot6334654557:AAE9uBbMvWfTAP6N4L57VIdX38ZLFPQZ9FM/sendmessage?chat_id=6034643381&text={txt.txt_answer_support}'),
        types.InlineKeyboardButton(
            text="Список из БД",
            callback_data=nomAdmin.pack(),
        ))
        #reply_markup=builder.as_markup())
        await message.answer(
        f'Вы хотели Админу написать?\nПрямо сейчас вставте в начало вашего сообщения\nзтот номер "{nomAdmin.u}" и нажмите отправить!\n\n_--_',
        reply_markup=builder.as_markup())
    else:
        await message.answer(
        f'Вы хотели Админу написать?\nПрямо сейчас вставте в начало вашего сообщения\nзтот номер "{nomAdmin.u}" и нажмите отправить!\n\n_--_',
        reply_markup=get_reply_keyboard1()
        )

from aiogram.utils.markdown import hide_link

@form_router.message(GetAdminFilter())
async def message_admin(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
    entities = [MessageEntity(type='bot_command', offset=10, length=8, url='/help@avtoposter_ro_bot')]
            # builder.add(types.InlineKeyboardButton(
            # text="🔥-- Погнали --🔥",
            # url="https://t.me/notcoin_bot?start=rp_9938433")
            # )
    user_b = await bot.get_me()
    text = message.text[5:]
    bot582 = Bot("5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M")
    #requests.get(f'https://api.telegram.org/bot5822305353:AAHexHNC9TLD1HZvZGcMg4C19hGnVGLyr6M/sendmessage?chat_id=5146071572&text={new_user_str}')
    await bot582.send_message(5146071572, text=f"Сообщение!!!\n\nBot:\n{user_b.username},\nот подпиcчика {message.from_user.first_name}\n" + text)

    await message.answer(
        **txt.content_adm.as_kwargs(),
        # '<u>Вам скоро ответят! Спасибо что вы с нами!\n\nСправочный гид -> /info_gid/u<>\n\n_--_',
        #  parse_mode=ParseMode.HTML, entities=entities,

        reply_markup=get_reply_keyboard1(),
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
    await state.storage.set_data('TgUser', {'donate': True})

    await message.answer(
        "Добро пожаловать, у вас полный доступ к действующему функционалу\nЗадавайте вопросы, делитесь мнениями...\n\nДалее обращай внимание на кнопки 😁",

        reply_markup=get_reply_keyboard1(),
    )

@form_router.message(Command(commands=["donate"]))
async def command_donate(message: Message, state: FSMContext) -> None:
    #await state.set_state(Form.name)
   #global is_donat
    #is_donat = True
    await message.answer(
        "Приветствем вас, ждите перевода на страницу оплаты...",

        reply_markup=get_reply_keyboard1(),
    )

@form_router.message(Command(commands=["get_vakancy"]))
async def command_get_vakancy(message: Message, state: FSMContext) -> None:
    # url = 'https://fastapi-pgstarterkit-test.onrender.com/status'
    # headers = {
    # 'accept': 'application/json',
    # 'Content-Type': 'application/x-www-form-urlencoded'}
    # payload = {"username": 'hansrubinok@yahoo.com', "password": "supersecretpassword"}
    # res = requests.get(url)#, headers=headers, data=payload)
    # res_d = res.json()
#***************
    cb360.url = "https"
    MyCallback.url = "http"

    print(217, cb360.foo, cb360.url, MyCallback.url)
    return

#*************************************
    url = 'https://www.youtube.com/watch?v=UM9OK9vFfRM'
    # работать можно с различными списками

    copyTube = MyUniTuber(filename='NOTCOIN.mp4')
    htm= await copyTube.get_Tube(url)
    #*****************************************
    print(208, htm[0], htm[1])
    video = types.FSInputFile(htm[0]+"\\"+htm[1], htm[1])
    await message.answer_video(video, caption="Видео без рекламы", reply_markup=ReplyKeyboardRemove())
#*********************************************

#@form_router.message(F.text.startswith("https://www.youtu"))
@form_router.message((F.chat.func(lambda chat: chat.type == 'private') & (F.text == "🔥 Бонусные-возможности")) | (F.chat.func(lambda chat: chat.type == 'private') & (F.text.startswith("https://youtu") | F.text.startswith("http://youtu"))))
async def tube_handler(message: types.Message, state: FSMContext) -> None:
    _is_donat=get_tguser(message.from_user.username).is_donate
    is_donat=get_tguser(message.from_user.username).is_donate
    if ((str(message.text).find('/promo') != -1) or (_is_donat == False)) :
        await message.answer(
            "Неправильно набрана команда, повторите!\n или введите полученный промокод",
            reply_markup=get_reply_keyboard1())
        return
# 'https://www.youtube.com/watch?v=UM9OK9vFfRM'

    if message.text.startswith("https://youtu") == False:

        await message.answer("Привет Youtube!\nТак назывыется новый функционал, позволяющий 'по кнопке'\nпосмотреть или послушать желаемое видео\nс Youtube, без назойливой рекламы...(3 клавиши - 3 режима.)\n\n->>> Просто вставь ссылку на видео в поле текстового сообщения <<<- ->>> далее следуй по инструкции <<<-",
         reply_markup=get_reply_keyboard1())
        return
    #await message.answer("Видео без рекламы", reply_markup=ReplyKeyboardRemove())
    url = message.text 
    cb360.url = url 
    cb720.url = url
    audio.url = url
    if message.video:
        await bot.delete_message(message.chat.id, message.message_id )
        await bot.send_message(message.chat.id, url)

    print(248, cb360.url)
    await message.answer(
    "Привет Youtube!\n720dpi - для настольных ПК\n360dpi - для мобильных\nАудио - для гурманов\n->>>Выбирай, жми и ожидай<<<- ",
    #reply_markup=get_inline_keyboard_creat(t1="360dpi",  delet=1))
    reply_markup=get_inline_keyboard_creat(t1="Video+Audo 720dpi", t2="Video+Audo 360dpi", t3="Only Audio" , t4="Далее", delet=2))


@form_router.message(F.chat.func(lambda chat: chat.type == 'private') & ~F.text.startswith("https://youtu"))
async def process_write_menu2_bots(message: types.Message, state: FSMContext) -> None:

    user_name = message.from_user.username
    first_name = message.from_user.first_name
    if message.text == None:
        print(121, message)
        return
    # if tg_user_is_db(user_name) != False:
    #     await save_newuser(message.from_user)
    print(message)
    _is_donat=get_tguser(user_name).is_donate
    if ((str(message.text).find('/promo') != -1) or (_is_donat == False)) :
        await message.answer(
            "Неправильно набрана команда, повторите!\n или введите полученный промокод",
            reply_markup=ReplyKeyboardRemove())
        return
    else:
        if message.text.startswith("https://") == True:
            await message.answer(
                "Эта ссылка не video_link",
                    reply_markup=get_reply_keyboard1())
            return
        # Получаем и обрабатываем сообщение 
        response = "Приват" # OpenaiFreeLast.get_answer_ofl(message.text, first_name=first_name)
        answer=response # 'Ответ HelperGPT:\n' + response['choices'][0]['text']

        await message.answer(
            answer,
                reply_markup=get_reply_keyboard1())

@form_router.message( F.chat.func(lambda chat: chat.type == 'supergroup'), F.poll)
async def process_talk_bots(message: types.Message, state: FSMContext) -> None:
    await message.answer_poll(question=message.poll.question, options=["монета", "токен"],  is_anonymous=False, correct_option_id=1, reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, message.message_id)
    await state.set_state(QuizAnswer.waiting_for_answer)
    print(222)

@form_router.message( F.chat.func(lambda chat: chat.type == 'supergroup'))
async def process_talk_bots(message: types.Message, state: FSMContext) -> None:
    # await state.clear()
    user_name = message.from_user.username
    if tg_user_is_db(user_name) == False:
        new_user_dict = dict(await save_newuser(message.from_user))
        add_tg_user(new_user_dict)
    # Получаем и обрабатываем сообщение 
    #response = OpenaiFreeLast.get_answer_ofl(message.text)
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
    print(255)
    respon = f"Эй, друг как тебя, повтори ка будь добр вопрос, а то я пока курил на балконе, с темы походу соскочил ..."
    answer=respon #'Ответ HelperGPT:\n' + response['choices'][0]['text']

    await message.answer(
        answer,
            reply_markup=ReplyKeyboardRemove())

#*******************************************poll_handler



#************************обработчик  of HTML
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from aiogram.methods import AnswerWebAppQuery
from aiogram.utils.web_app import safe_parse_webapp_init_data, check_webapp_signature, parse_webapp_init_data
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    WebAppInfo,
)


async def ext_send_message_handler(request: Request):
    bot1: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    promokod = data["msg_id"]
    receiver = web_app_init_data.receiver
    #await bot1.send_message(receiver.id, f"/promo-{promokod}")
    #SentWebAppMessage = await bot1.answer_web_app_query(web_app_init_data.query_id, result=)
    # reply_markup = None
    # if data["with_webview"] == "1":

    await bot.answer_web_app_query(
        web_app_query_id=web_app_init_data.query_id,
        result=InlineQueryResultArticle(
            id=web_app_init_data.query_id,
            title="Demo",
            input_message_content=InputTextMessageContent(
                message_text=f"/promo-{promokod}",
                parse_mode=None,
            ),
            reply_markup=None,
        ),
    )
    return json_response({"ok": True}) 

async def get_vakancy_handler(request: Request):
    bot1: Bot = request.app["bot"]
    data = await request.post()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot1.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    print(382, data["msg_id"])
    kot = str_for_dict(data["msg_id"]) #parse_webapp_init_data(init_data=data["_auth"],  loads=[data["msg_id"]])

    print(kot)

    #return json_response({"ok": True, "data": kod})
    # {"category":"Менеджер по продажам","URL_vacancy":"https://rabota.by/vacancies/menedzher_po_prodazham",
    # "days_ago":"5","quantity_get_vacancy":"3","number_of_pages":"3","ID_chat":5146071572}

    #receiver = web_app_init_data.receiver
    url = 'https://fastapi-pgstarterkit-test.onrender.com/api/v1/login/access-token'
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {"username": 'hansrubinok@yahoo.com', "password": "supersecretpassword"}
    res = requests.post(url, headers=headers, data=payload)
    res_d = res.json()['access_token']

    url2 = f"https://fastapi-pgstarterkit-test.onrender.com/api/v1/services/quere-new-vakamcy/"
    headers1 = {
    'accept': 'application/json',
    'Authorization': f"Bearer {res_d}",
    'Content-Type': 'application/json'
    }
    
    payload1 = {
    "kategory": kot['category'],#"Менеджер по продажам",
    "url": kot['URL_vacancy'],#'https://rabota.by/vacancies/menedzher_po_prodazham',
    "page": int(kot['number_of_pages']),
    "fd": int(kot['days_ago']),
    "max_count_vacancy": int(kot['quantity_get_vacancy']),#1,
    "chat_id": int(kot['ID_chat']),#5146071572,
    "bot_token": TELEGRAM_BOT_TOKEN
    }
    data2 = json.dumps(payload1)
    print(473, payload1, data2)
    message_text_out = ""
    list_mess_id = []
    try:
        #list_res = []

        res = requests.post(url2, headers=headers1, json=json.loads(data2))
        print(474, res.text)
        res_j = json.loads(res.text)
        print(490, res_j)
        if res_j == []:
            return json_response({"ok": True, "data": "На сегодня обновления отсутствуют ", 'message_id': 1}) 
        for out_txt in res_j:
            print(492, type(out_txt), out_txt)

            #print(375, 177, res.text)
            payload2 = {
                'ID вакансии': out_txt['id_vakancy'],
                'Категория': out_txt['kategory'],
                'Наименование vakancy': out_txt['name'],
                'Компания': out_txt['company'],
                'Заработок': out_txt['price'],
                #'message_id': out_txt['message_id'],
                #'Краткое описание':         out_txt['description_short'],
                #'link_vakancy': res.json()[link_vakancy],
                #'Подробное описание': res.json()[description_full],
                'Дата размещения': out_txt['date_publikate'],
            }
            list_mess_id.append(out_txt['mess_id'])
            message_text = "\n".join([f"{key}: {value}" for key, value in payload2.items()])
            message_text_out += "\n------------\n\n" + message_text
        message_text_out1 = "Новые вакансии\n" + message_text_out
    except requests.exceptions.HTTPError as HTTPError:
        #print(375, 177, res.text)
        return json_response({"ok": False, "data": res.status_code})
    # await bot.answer_web_app_query(
    #     web_app_query_id=web_app_init_data.query_id,
    #     result=InlineQueryResultArticle(
    #         id=web_app_init_data.query_id,
    #         title="Demo",
    #         input_message_content=InputTextMessageContent(
    #             message_text="Запрос в обработке\nобычно занимает не более2 мин.\nа пока обратите внимание на наши новинки",
    #             parse_mode=None,
    #         ),
    #         reply_markup=None,
    #     ),
    # )
    # keyword=str(out_txt['id_vakancy'])
    # chat_id=-1002040372211
    # mess_id = get_message_id_by_keyword(chat_id, keyword, 10) or 1
    # message_id = 1 #out_txt['mess_id'] if out_txt['mess_id'] != 1 else mess_id
    print(509, list_mess_id)
    return json_response({"ok": True, "data": message_text_out1, 'message_id': list_mess_id}) 

async def check_data_handler(request: Request):#, state: FSMContext):
    bot: Bot = request.app["bot"]
    stor: MemoryStorage = request.app["storage"]
    data = await request.post()
    #print(550, stor.)

    tg_user = parse_webapp_init_data(init_data=data["_auth"]).user

    ch = await stor.get_data('TgUser')
    print(554, ch)
    # if ch["donate"]:
    #     print(555, tg_user)
    #     if check_webapp_signature(bot.token, data["_auth"]):
    #         return json_response({"ok": True, "donate": ch['donate']})
    if check_webapp_signature(bot.token, data["_auth"]):
        return json_response({"ok": True, "donate": ch['donate']})
    return json_response({"ok": False, "err": "Unauthorized"}, status=401)
#**************************END

async def check_box_video_handler(request: Request):
    bot: Bot = request.app["bot"]
    data = await request.post()
    if check_webapp_signature(bot.token, data["_auth"]) is False:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)

    kod = json.loads(data["msg_id"]) #parse_webapp_init_data(init_data=data["_auth"],  loads=[data["msg_id"]])
    print(560, data['msg_id'])


    return json_response({"ok": True})

#**************************END
#cb360 = MyCallback(foo="360dpi", url="-").unpack()

#**********************---CALLBACK --**********
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.callback_data import CallbackData


@cal_router.callback_query(F.data == "video:Continue:-")
async def send_value2(callback: CallbackQuery):
    print("458, llll")
    sufix = callback.data.split("_")[1]

    if sufix == "start":
        print(206, )
        if ( sufix[0]== "\n@") | ( sufix[1]== ''):
            await callback.message.answer(
                """ __--__\n\nНачните с добавления канала для администрирования\n\n
                Чтобы добавить канал, вы должны выполнить два следующих шага:\n\n
                1. Добавьте @cripto_fack_new_bot в администраторы вашего канала.\n
                2. Перешлите мне любое сообщение из вашего канала (вы также можете отправить @username или Group ID) """,
                #show_alert=True
            )
            Mode_select_channel_admin=True
            return
        await callback.message.answer(
            f"""У вас подключены следующие каналы:{[0]} они в списке администрируемых каналов. 
                """,
            reply_markup=get_inline_keyboard_creat())
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[]) )

##****---END --- CONTINUE---

@cal_router.callback_query(F.data.startswith("video:")) #Text(startswith="video_"))
async def run_repost_plus(callback: CallbackQuery):
    bot_token = TELEGRAM_BOT_TOKEN
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    sufix_full=callback.data.split(":") or ['', '', '']
    print(501, sufix_full[1])
    print(485, cb360.url, cb360.u)

    if (sufix_full[1] == "bd"):
        message_text_out=""
        list_tguser_username = load_users()
        for item in list_tguser_username:
            message_text = "\n".join([f"{key}: {value}" for key, value in item.items()])
            message_text_out += "\n------------\n\n" + message_text

        await callback.answer(text=f"_--_\n\nСпасибо, что воспользовались ботом! ")

        await callback.message.answer(
            f"""Users:\n\n{message_text_out}. 
                """,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[]) )
        await bot.delete_message(chat_id, message_id-2 )
        await bot.delete_message(chat_id, message_id-1 )
        await bot.delete_message(chat_id, message_id )
    #сделать удаление 3-х предыдущих
        return
    elif sufix_full[1] != "continue":
        if sufix_full[1] == "Audio":
            url = audio.url
            dpi = 0
        if sufix_full[1] == "360dpi":
            dpi = 360 
            url = cb360.url
        if sufix_full[1] == "720dpi":
            dpi = 720 
            url = cb720.url
        await callback.answer(text=f"_--_\n\nСпасибо, что воспользовались ботом!\nОн в процессе закачки...\nVideo: {url} ",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[]) )
        copyTube = MyUniTuber(chat_id=chat_id, bot_token=bot_token)#filename='NOTCOIN.mp4')
        htm= await copyTube.get_Tube(url, dpi=dpi, u=cb360.u)
        thumbnail = types.URLInputFile(htm[3])
        if cb360.u == 1:
            await bot.send_video(chat_id, htm[2], thumbnail=thumbnail,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[]) )
            print(208, htm[2], htm[3])
            return
        video = types.FSInputFile(htm[0])
        await bot.delete_message(chat_id, message_id-2 )
        await bot.delete_message(chat_id, message_id-1 )
        await bot.delete_message(chat_id, message_id )
        mess = await bot.send_video(chat_id, video, thumbnail=thumbnail, caption="Видео без рекламы",
        reply_markup=get_inline_keyboard_creat(t1="Video+Audo 720dpi", t2="Video+Audo 360dpi", t3="Only Audio" , t4="Далее", delet=2))
        os.remove(htm[0])

        #print(533, mess)
    else:
        print(528, callback.message.chat.id, callback.message.message_id-1)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,  reply_markup=InlineKeyboardMarkup(inline_keyboard=[]) )
        # await bot.delete_message(callback.message.chat.id, callback.message.message_id-2 )
        # await bot.delete_message(callback.message.chat.id, callback.message.message_id-1 )
        # await bot.delete_message(callback.message.chat.id, callback.message.message_id )

        await callback.message.answer(
        "Вы можете также задать вопрос или изучите мои возможности\n\n/help\n\n Кстати уважаемые пользователи иногда скидывают полезную информацию",#"Привет Youtube!\nПросто пришли ссылку на видео в виде текстового сообщения.",
        #reply_markup=get_inline_keyboard_creat(t1="360dpi",  delet=1))
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))
        time.sleep(15)
        builder.add(types.InlineKeyboardButton(
            text="🔥-- Погнали --🔥",
            url="https://t.me/notcoin_bot?start=rp_9938433")
            )
        await bot.send_video(chat_id, video='BAACAgIAAxkBAAIHZWWqLQvHaT8sxAqwFy6VjUzn4YuCAAL_PgACRphRSc3X5bCE-d64NAQ', width=480, caption="Информация для любителей поиграть.\n\nСуть: накапливать монеты Notcoin, используя простые действия - клики по экрану мобилы.Короче попробуй сам....\n (от меня бонус - 25000 монет, кстати монеты набирают популярность!)",
         reply_markup=builder.as_markup())