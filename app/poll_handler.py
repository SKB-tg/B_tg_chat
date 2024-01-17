from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram import methods
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.strategy import FSMStrategy, apply_strategy

class QuizAnswer(StatesGroup):
    waiting_for_answer = State()

# Устанавливаем соединение с OpenAI API 

p_router = Router()
# инициализируем словарь для хранения результатов викторины
quiz_results = {}
users=[]
@p_router.poll_answer()#StateFilter("QuizAnswer:waiting_for_answer"))
async def handle_correct_answer(message: types.PollAnswer, state: FSMContext, bot):

    data = await state.get_data()
    st = await state.get_state()
    print(14, data)#, Current_chat_id)
    users.append(message.user)
# заполняем словарь ключами - порядковыми номерами пользователей
    for user in users:
        quiz_results[user.id] = 0

    # проверяем, что это правильный ответ на викторину
    if message.option_ids == [1]:
        # получаем порядковый номер пользователя
        user_id = message.user.id
        # увеличиваем количество правильных ответов пользователя в словаре
        quiz_results[user_id] += 1
        # проверяем, достиг ли пользователь финишного номера
        if quiz_results[user_id] == 1:#FINISH_NUMBER:
            # отправляем поздравление пользователю
            await bot.send_message(data.get("CH_ID"), f"Поздравляем, {message.user.first_name}! Вы первый ответили правильно на все вопросы!")
    else:
        # если ответ неправильный, просто игнорируем его
        pass
    # await message.answer_poll(question=message.poll.question, options=["монета", "токен"],  is_anonymous=False, reply_markup=types.ReplyKeyboardRemove())
    # await message.delete(message.chat.id, message.message_id)


# 177 id='5454302526809572777' question='PollAnswer' options=[PollOption(text='5',
#  voter_count=0), PollOption(text='2', voter_count=0)] total_voter_count=0 is_clo
# sed=False is_anonymous=True type='quiz' allows_multiple_answers=False correct_op
# tion_id=None explanation=None explanation_entities=None open_period=None close_d
# ate=None


# 177 message_id=309 date=datetime.datetime(2023, 12, 10, 16, 28, 2, tzinfo=TzInfo
# (UTC)) chat=Chat(id=-1001849731160, type='supergroup', title='Crypto_bag-chat',
# username=None, first_name=None, last_name=None, is_forum=None, photo=None, activ
# e_usernames=None, emoji_status_custom_emoji_id=None, emoji_status_expiration_dat
# e=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_mess
# ages=None, join_to_send_messages=None, join_by_request=None, description=None, i
# nvite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None, me
# ssage_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_m
# embers=None, has_protected_content=None, sticker_set_name=None, can_set_sticker_
# set=None, linked_chat_id=None, location=None) message_thread_id=None from_user=U
# ser(id=777000, is_bot=False, first_name='Telegram', last_name=None, username=Non
# e, language_code=None, is_premium=None, added_to_attachment_menu=None, can_join_
# groups=None, can_read_all_group_messages=None, supports_inline_queries=None) sen
# der_chat=Chat(id=-1001663436185, type='channel', title='Crypto_bag', username='c
# rypto_bag_develop', first_name=None, last_name=None, is_forum=None, photo=None,
# active_usernames=None, emoji_status_custom_emoji_id=None, emoji_status_expiratio
# n_date=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video
# _messages=None, join_to_send_messages=None, join_by_request=None, description=No
# ne, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=Non
# e, message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hid
# den_members=None, has_protected_content=None, sticker_set_name=None, can_set_sti
# cker_set=None, linked_chat_id=None, location=None) forward_from=None forward_fro
# m_chat=Chat(id=-1001663436185, type='channel', title='Crypto_bag', username='cry
# pto_bag_develop', first_name=None, last_name=None, is_forum=None, photo=None, ac
# tive_usernames=None, emoji_status_custom_emoji_id=None, emoji_status_expiration_
# date=None, bio=None, has_private_forwards=None, has_restricted_voice_and_video_m
# essages=None, join_to_send_messages=None, join_by_request=None, description=None
# , invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None,
#  message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidde
# n_members=None, has_protected_content=None, sticker_set_name=None, can_set_stick
# er_set=None, linked_chat_id=None, location=None) forward_from_message_id=482 for
# ward_signature=None forward_sender_name=None forward_date=datetime.datetime(2023
# , 12, 10, 16, 27, 59, tzinfo=TzInfo(UTC)) is_topic_message=None is_automatic_for
# ward=True reply_to_message=None via_bot=None edit_date=None has_protected_conten
# t=None media_group_id=None author_signature=None text=None entities=None animati
# on=None audio=None document=None photo=None sticker=None story=None video=None v
# ideo_note=None voice=None caption=None caption_entities=None has_media_spoiler=N
# one contact=None dice=None game=None poll=Poll(id='5454302526809572795', questio
# n='send_message', options=[PollOption(text='5', voter_count=0), PollOption(text=
# '3', voter_count=0)], total_voter_count=0, is_closed=False, is_anonymous=True, t
# ype='quiz', allows_multiple_answers=False, correct_option_id=None, explanation=N
# one, explanation_entities=None, open_period=None, close_date=None) venue=None lo
# cation=None new_chat_members=None left_chat_member=None new_chat_title=None new_
# chat_photo=None delete_chat_photo=None group_chat_created=None supergroup_chat_c
# reated=None channel_chat_created=None message_auto_delete_timer_changed=None mig
# rate_to_chat_id=None migrate_from_chat_id=None pinned_message=None invoice=None
# successful_payment=None user_shared=None chat_shared=None connected_website=None
#  write_access_allowed=None passport_data=None proximity_alert_triggered=None for
# um_topic_created=None forum_topic_edited=None forum_topic_closed=None forum_topi
# c_reopened=None general_forum_topic_hidden=None general_forum_topic_unhidden=Non
# e video_chat_scheduled=None video_chat_started=None video_chat_ended=None video_
# chat_participants_invited=None web_app_data=None reply_markup=None

#answer_poll
# 14 poll_id='5467809863948043396' option_ids=[1] voter_chat=None user=User(id=5146071572, is_bot=False, first_name='Kirill-79', last_name=None, username='kirill7979', language_code='ru', is_premium=None, added_to_attachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supports_inline_queries=None)
# 14 poll_id='5467809863948043396' option_ids=[1] voter_chat=Chat(id=-100184973116
# 0, type='supergroup', title='Crypto_bag-chat', username=None, first_name=None, l
# ast_name=None, is_forum=None, photo=None, active_usernames=None, emoji_status_cu
# stom_emoji_id=None, emoji_status_expiration_date=None, bio=None, has_private_for
# wards=None, has_restricted_voice_and_video_messages=None, join_to_send_messages=
# None, join_by_request=None, description=None, invite_link=None, pinned_message=N
# one, permissions=None, slow_mode_delay=None, message_auto_delete_time=None, has_
# aggressive_anti_spam_enabled=None, has_hidden_members=None, has_protected_conten
# t=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None, lo
# cation=None) user=User(id=136817688, is_bot=True, first_name='Channel', last_nam
# e=None, username='Channel_Bot', language_code=None, is_premium=None, added_to_at
# tachment_menu=None, can_join_groups=None, can_read_all_group_messages=None, supp
# orts_inline_queries=None)

#poll
# 57 id='5467580972255939532' question='p_router.poll_answer' options=[PollOption(
# text='монета', voter_count=0), PollOption(text='токен', voter_count=1)] total_vo
# ter_count=1 is_closed=False is_anonymous=False type='regular' allows_multiple_an
# swers=False correct_option_id=None explanation=None explanation_entities=None op
# en_period=None close_date=None

# 555 {'storage': defaultdict(<class 'aiogram.fsm.storage.memory.MemoryStorageRecord'>, 
#{StorageKey(bot_id=6334654557, chat_id=-1001849731160, user_id=-1001849731160, thread_id=None, destiny='default'): MemoryStorageRecord(data={'options': ['монета', 'токен'], 'correct_option_id': 1, 'CH_ID': -1001849731160}, state='Quiz
# Answer:waiting_for_answer'), StorageKey(bot_id=6334654557, chat_id=136817688, us
# er_id=136817688, thread_id=None, destiny='default'): MemoryStorageRecord(data={}
# , state=None)})}