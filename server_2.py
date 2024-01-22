"""Сервер Telegram бота, запускаемый непосредственно"""
import time
import asyncio
from asyncio import Lock
import logging
import os
from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO
from dotenv import load_dotenv
from aiogram.types.update import Update
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiohttp.web import run_app, static
from aiohttp.web_app import Application
from aiogram.fsm.storage.memory import MemoryStorage, StorageKey
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.strategy import FSMStrategy
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiogram import BaseMiddleware
from aiogram.utils.chat_action import ChatActionMiddleware, ChatActionSender
from aiogram.dispatcher.flags import get_flag

from aiogram import Bot, Dispatcher#, types, F, Router, html # executor,
from async_timeout import timeout
import requests
from app.bot_handlers import (bot, form_router, base_url, ext_send_message_handler,
    check_data_handler, get_vakancy_handler, cal_router)
from app.poll_handler import handle_correct_answer, p_router, QuizAnswer

PORT = os.getenv("PORT")

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



async def main_rout(request: Request):
    return FileResponse(Path(__file__).parent.resolve() / "./app/index.html")
    print(Path(__file__).parent.resolve())

async def on_startup(bot: Bot, base_url: str):
    await bot.delete_webhook()
    await bot.set_webhook(f"{base_url}/webhook", allowed_updates=["message", "edited_channel_post", "callback_query", "poll_answer"])

#*********************************************
from app.bot_utils import save_fsm_storage_chat_id
from aiogram import BaseMiddleware
class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        data = await save_fsm_storage_chat_id(data)
    #*******#Запись "CH_ID" текущего канала в виде dict в хранилище ( data или state) для 
    # дальнейшего использ-я вызывается CH_ID = await state.get_data()["CH_ID"] при сполз. state: FSMContext
        print(73, event.update_id)
        result=await handler(event, data)
        return result


#******************

def main():
    #bot = Bot("6163364880:AAGSbyRC5avfSuSzCn3whB5vcvwL2QS5mlc")
    #form_router = Router
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    #requests.get('https://api.telegram.org/bot6334654557:AAE9uBbMvWfTAP6N4L57VIdX38ZLFPQZ9FM/sendmessage?chat_id='+str(5146071572)+'&text=start.')
    dp.include_routers(cal_router, form_router, p_router)
    dp.update.outer_middleware(SomeMiddleware())
    #dp.message.middleware(ChatActionMiddleware())
    #dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True, show_alert=True))

    app = Application()
    dp["base_url"] = base_url
    app["bot"] = bot
    dp.startup.register(on_startup)

    #https://api.telegram.org/bot6334654557:AAE9uBbMvWfTAP6N4L57VIdX38ZLFPQZ9FM/Webhookinfo
    #update = Update.model_validate(await request.json(), context={"bot": bot})
    #dp.feed_update(bot=bot, update=update)
    #await on_startup(bot, base_url)
    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    SimpleRequestHandler(
        dispatcher=dp, bot=bot,
    ).register(app, path="/webhook")
    app.router.add_get("/", main_rout)
    app.router.add_post("/get_vakancy", get_vakancy_handler) # в более сложном варианте запихнуть в ф router.py
    app.router.add_post("/ext_message", ext_send_message_handler) # в более сложном варианте запихнуть в ф router.py
    app.router.add_post("/checkData", check_data_handler)
    app.router.add_static("/static", Path("./static"))

    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=PORT)

if __name__ == '__main__':
    main()
