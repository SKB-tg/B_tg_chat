import asyncio
import time
#from g4f_home import OpenaiFree
from app import g4f_st
#from g4f_st import ChatCompletion
import g4f
from g4f.Provider import (
    AItianhu, # ошибки по кукам
    Aichat,# ошибки по кукам
    Bard, # тоже куки
    Bing, # видно браузерный вариант треб ssl
    ChatBase,# не для болтовни. ответ на англ
    ChatgptAi, # на уровне You может даже на балл серьезне(но не точно)
    OpenaiChat,# опять куки
    Vercel, # разрывает соед.
    GptGo, # ответ на рус. юмор неплохой, показалось - на балл серьезнее чем getgpt
    Yqcloud, # похоже на ChatgptAi (ввежливый аж противно)
    Theb, # опять куки
    GPTalk, # на уровне You
    ChatAiGpt,

)
nn=1

class OpenaiFreeLast():
	promt: str = ""

	@staticmethod
	def get_answer_ofl(promt, first_name="неунывающий Саморитянин"):
		global nn
		nn +=  1
		model = 'gpt-3.5-turbo'
		text=f"На тему этой фразы дай совет коротко, конкретно, но в шутливом, несерьезном стиле: '{promt}'"
		#text=f"На тему этой фразы дай реплику коротко, конкретно, но в ворчливом, поучительном стиле: '{promt}'"


		if nn%3 == 0:
			print("----------GPTalk---------------")
			messages=[#{"role": "system", "content": "Ты Виктор - настоящий чат-бот с веселым характером, на вопросы и реплики даешь совет лаконично, но с сарказмом, в легком стиле."},
			 #{"role": "user", "content": "Какая столица Италии?"},
			 #{"role": "assistant", "content": "Рим, как будто все это еще не знают. Да и тебе давно пора выучить."},
			 {"role": "user", "content": promt}]
			response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo,
			provider=g4f.Provider.GptGo,
			messages=messages) #[{"role": "user", "content": text}])
			return response

		elif nn%2 == 0:
			print("----------ChatgptAi---------------")
			messages=[{"role": "system", "content": "Вы, Платон, мудрый чат-бот, но в то же время сварливый и немногословный на единственный последующий ответ."}, {"role": "user", "content": promt}]
			response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo,
			provider=g4f.Provider.ChatgptAi,
			messages=messages)

			col=len(response)
			response_out = f"{response[:-((col//5)*0)]} ...."
			return response_out

		elif nn%1 == 0:
			#text=promt
			#text=f"На тему этой фразы дай совет коротко, конкретно, но в шутливом, несерьезном стиле: '{promt}'"
			#response = g4f_st.ChatCompletion.create(messages=messages, provider=GetGpt)
			#text="Продолжи список 'народных поговорок' и 'мудрых наблюдений' на тему 'богач, бедняк и благотворительность': 'скупой платит дважды', 'не имей сто рублей, а имей сто друзей', 'не жалей на доброе дело, кто знает как жизнь повернётся'."
			#messages=[{"role": "system", "content": "Вы Мичо - настоящий чат-бот с веселым характером, на вопросы и замечания отвечаете лаконично, но в юмористическом, легкомысленном стиле."}, {'role': 'user', 'content': text}]
			# response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo,
			# provider=g4f.Provider.ChatgptAi,
			# messages=messages)
			response = g4f_st.ChatCompletions.create(model=model, messages=[{'role': 'user', 'content': promt}])
			answer = ""
			for message in response:
				answer += str(message) 
			print(44, answer, response)
			if len(answer) < 5:
				time.sleep(1)
				response = f"Эй, друг как тебя, аx вот {first_name}, повтори ка будь добр вопрос, а то я пока курил на балконе, с темы походу соскочил ..."
				return response
				# response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo,
				# provider=g4f.Provider.You,
				# messages=[{'role': 'user', 'content': text}])
				# response_out = response.split('"')[1]
			#return "response"





# messages": [{"role": "system", "content": "Марв — настоящий чат-бот, который к тому же саркастичен."}, {"role": "user", "content": "Какая заглавная буква Франции?"}, {"role": "assistant", "content": "Париж, как будто все это еще не знают."}]}
# {"messages": [{"role": "system", "content": "You Platon are a wise chat bot, but at the same time grumpy and laconic in your answers."}, {"role": "user", "content": text}, {"role": "assistant", "content": "О, просто какой-то парень по имени Уильям Шекспир. Слышали о нем когда-нибудь?"}]}
# {"messages": [{"role": "system", "content": "Ты Platon - мудрый чат-бот, но при этом ворчливый и лаконичный в ответах."}, {"role": "user", "content": "Как далеко Луна с Земли?"}, {"role": "assistant", "content": "Около 384 400 километров. Плюс-минус несколько, это действительно имеет значение."}
#Вы Мачо - настоящий чат-бот с веселым характером, на вопросы и замечания отвечаете лаконично, но в юмористическом, легкомысленном стиле.
#Эй, друг как тебя, а вот Юра повторика будь добр вопрос, а то я пока курил на балконе, с темы общения походу соскочил ...
#You are Macho - a real-chat bot with a cheerful character, you answer questions and remarks laconically, but in a humorous, frivolous style."
#, "content": "You Platon are a wise chat-bot, but at the same time grumpy and laconic for the only subsequent response
