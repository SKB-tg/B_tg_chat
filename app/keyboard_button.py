from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    MenuButtonCommands,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
    BotCommand,
    MessageEntity,
    Update,
    KeyboardButtonRequestChat,
)

#**********************---CALLBACK --**********
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="video"):
    foo: str = "360dpi"
    url: str = ""
    u: int = 0
cb720 = MyCallback(foo="720dpi")
cb360 = MyCallback(foo="360dpi")
audio = MyCallback(foo="Audio")
Continue = MyCallback(foo="continue")

print(29, cb360.pack())


def get_inline_keyboard_creat(t1: str="Далее", t2: str="Далее", t3: str="Далее", t4: str="Далее",
                        t5: str="Далее",t6: str="Далее", call_data=cb720.pack(),
                        call_data1=cb360.pack(), call_data2=audio.pack(),
                        call_data3=Continue.pack(), delet=0):

    def but(n: str='1', call_data: str=""):
        return InlineKeyboardButton(text=f"{n}", callback_data=call_data)
    buttons =[
            [InlineKeyboardButton(text=f"{t1}", callback_data=f"post-create_media_{call_data}")],
            [InlineKeyboardButton(text=f"{t2}", callback_data="post-create_continue"),
            InlineKeyboardButton(text=f"{t3}", callback_data="PPP")],
            [InlineKeyboardButton(text=f"{t4}", callback_data="Edit")],
            [InlineKeyboardButton(text="Титры с Youtube", callback_data=f"video-create_youtube_{call_data}")],
            [InlineKeyboardButton(text="Удалить сообщение", callback_data=f"post-create_delete_{call_data}"),
            InlineKeyboardButton(text="Далее", callback_data=f"post-create_continue_{call_data}")]
        ]
    #print(561, delet)
    if delet > 2:
        buttons.pop(delet-1)
        #print(buttons)
    if delet == 2:
            buttons =[
            [but(t1, call_data), but(t2, call_data1)], [but(t3, call_data2), but(t4, call_data3)]
            ]
    if delet == 1:
            buttons =[
            [but(t1, call_data)],
            ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_reply_keyboard4(t1="AI - модели", t2="Настройка", t3="🔥 Бонус-возможности", t4="Далее"):
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{t1}"), KeyboardButton(text=f"{t2}")],
        [KeyboardButton(text=f"{t3}"), KeyboardButton(text=f"{t4}")]],
        one_time_keyboard=False, resize_keyboard=True,
    )
    return reply_markup_buttons

def get_reply_keyboard2(t1="🔥 Бонус-возможности", t2="Далее"):
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{t1}"), KeyboardButton(text=f"{t2}")],
        ],
        one_time_keyboard=False, resize_keyboard=True,
        )
    return reply_markup_buttons

def get_reply_keyboard1(t1="🔥 Бонусные-возможности"):
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f"{t1}")],
        ],
        one_time_keyboard=False, resize_keyboard=True,
        )
    return reply_markup_buttons

def get_reply_keyboardRequestChat1(t1="🔥 Бонус-возможности"):
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButtonRequestChat(chat_is_channel =True, chat_has_username=True)],
        ],
        one_time_keyboard=False, resize_keyboard=True,
        )
    return reply_markup_buttons

def get_reply_keyboard0():
    reply_markup_buttons=ReplyKeyboardMarkup(
        keyboard=[],
        one_time_keyboard=False, resize_keyboard=True,
        )