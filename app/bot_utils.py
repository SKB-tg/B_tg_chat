from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO, cast
from aiogram.fsm.storage.base import BaseStorage

#from app.TeleBot import service_telethon

#MyStorage = BaseStorage()

#     vacancies_data = #await set_data( "vacancies_data", {"vacancies_mess_id": None} )

#mess_id = service_telethon.get_chat_history(-1002040372211)

# def get_message_id_by_keyword(chat_id, keyword: str, limit: int):
#     messages = service_telethon.scan_messages(chat_id, limit)
#     for message in messages:
#         print(15, message.text)
#         if keyword in message.text:
#             print(18, message)
#             return message.message_id
#         return 1

#   Используется в MyMiddleware 
async def save_fsm_storage_chat_id(data: Dict[str, Any]) -> Dict[str, Any]:
    #*******#Запись "CH_ID" текущего канала в виде dict в хранилище ( data или state) для дальнейшего использ-я
    user = data.get("event_from_user")
    chat = data.get("event_chat")
    chat_id_new = chat.id if chat else None
    user_id_new = user.id if user else None
    current_key = []
    #CH_ID = str(data["fsm_storage"].__dict__).split(",")[2].split("=")[1]
    #Current_Storage.data.update({"CH_ID": CH_ID})
    Current_Storage = data["fsm_storage"].storage
    for i in Current_Storage.keys():
        current_key.append(i)
    _chat_id_old=await data["fsm_storage"].get_data(current_key[-2]) if (len(current_key) > 1) else None
    if (_chat_id_old == None):
        chat_id_old = 0 
    else: 
        chat_id_old = _chat_id_old.get("CH_ID")
    if ((chat_id_new != None) & (chat_id_new != chat_id_old)) | (chat_id_old == 0):
        await data["fsm_storage"].update_data(current_key[-1], {"CH_ID": chat_id_new})
        if (len(current_key) > 2):
            data["fsm_storage"].storage.pop(current_key[-3]) #удаление чтобы не накапливалось
    else:
        await data["fsm_storage"].update_data(current_key[-1], {"CH_ID": chat_id_old})
        if (len(current_key) > 2):
            data["fsm_storage"].storage.pop(current_key[-3]) #удаление чтобы не накапливалось
    print(555, chat_id_old, chat_id_new, current_key[-1], data["fsm_storage"].__dict__) #Current_Storage.get("chat_id"))#, context.key)

    return data
