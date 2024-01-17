from typing import Callable, Dict, Any, Awaitable, Union, List, Optional, BinaryIO, cast


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
    print(555, chat_id_old, chat_id_new, current_key[-1], data["fsm_storage"].__dict__ ) #Current_Storage.get("chat_id"))#, context.key)

    return data