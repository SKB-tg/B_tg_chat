# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio

# # download and load all models
# preload_models()

# # generate audio from text
# text_prompt = """
#      Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
#      But I also have other interests such as playing tic tac toe.
# """
# audio_array = generate_audio(text_prompt)

# # save audio to disk
# write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# # play text in notebook
# Audio(audio_array, rate=SAMPLE_RATE)


#from aiogram.dispatcher import Dispatcher
#from aiogram.utils import executor

# bot = Bot(token='YOUR_TOKEN')
# dp = Dispatcher(bot)

# async def copy_video(url, chat_id):
#     response = requests.get(url, stream=True)
#     content_type = response.headers['Content-Type']
#     if 'video' not in content_type:
#         raise ValueError('URL does not contain a video')
#     video_file = io.BytesIO()
#     for chunk in response.iter_content(chunk_size=1024):
#         if chunk:
#             video_file.write(chunk)
#     video_file.seek(0)
#     video = types.InputFile(video_file)
#     await bot.send_video(chat_id, video)
import logging
import io
import requests

import os
import asyncio
from aiogram import Bot, types
from aiogram.types import BufferedInputFile, FSInputFile
    
from pathlib import Path
from typing import Callable, Dict, Any, List, Optional, BinaryIO, cast

#Инструкция - https://pytube.io/en/latest/user/streams.html#filtering-for-audio-only-streams
from pytube import YouTube, request

#***************************

####################################

class MyUniTuber:
	def __init__(self, 
		filename: str = None,
		filename_prefix: str = None,
		chat_id=None, bot_token=None,
	):
		self.filename = filename
		self.filename_prefix = filename_prefix
		self.chat_id = chat_id
		self.bot_token = bot_token
	async def get_Tube(self, url, dpi: int=360, u=0) -> list:
		yt = YouTube(url) #'https://youtu.be/HGc0uaB4LqQ?si=hD2SPhLwdz3ePDGV')
		stream_url = yt.streams.get_by_itag(18) if dpi == 360 else yt.streams.get_by_itag(22)
		if dpi == 0:
			stream_url = yt.streams.get_by_itag(140)
		thumbnail_url = yt.thumbnail_url
		bot = Bot(token=self.bot_token)
		if u == 1:
			return [0, 0, stream_url, thumbnail_url]
# 		#dp = Dispatcher(bot)
		output_path = str(Path.cwd()) + "\\out"
		if self.filename != None: #os.path.isfile(os.path.join(output_path, self.filename)):
			return [output_path, self.filename, "", thumbnail_url]
		video_file = stream_url.download(output_path=output_path, filename=self.filename )
		#with open(video_file, 'rb') as f:
		# video = types.FSInputFile(output_path, "NOTCOIN.mp4")
		# await bot.send_video(self.chat_id, video)
		return [video_file, yt.title + ".mp4", "",thumbnail_url]

# 		try:

# async def get_Tube(url, chat_id):
#*************************************
		# response = requests.get(url, stream=True)
		# content_type = response.headers['Content-Type']
		# if 'video' not in content_type:
		# 	raise ValueError('URL does not contain a video')
		# video_file = io.BytesIO()
		# for chunk in response.iter_content(chunk_size=1024):
		# 	if chunk:
		# 		video_file.write(chunk)
		# video_file.seek(0)
		# video = types.InputFile(video_file)
		# bot.send_video(self.chat_id, video)

#*********************************

			     #    self,
        # output_path: Optional[str] = None,
        # filename: Optional[str] = None,
        # filename_prefix: Optional[str] = None,
        # skip_existing: bool = True,
        # timeout: Optional[int] = None,
        # max_retries: Optional[int] = 0
	



# <Stream: itag="18" mim_type="video/mp4" res="360p" fps="25fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">, 
# <Stream: itag="22" mime_type="video/mp4" res"720p" fps="25fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">, 

#<Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False"
# ype="audio">, <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="m
# 4a.40.2" progressive="False" type="audio">, <Stream: itag="249" mime_type="audi
# /webm" abr="50kbps" acodec="opus" progressive="False" type="audio">, <Stream: i
# ag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False"
# ype="audio">, <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="
# pus" progressive="False" type="audio">]

async def main():
    bot_token = '6334654557:AAE9uBbMvWfTAP6N4L57VIdX38ZLFPQZ9FM'
    chat_id = 5146071572
    kategory = "Менеджер по продажам"
    url = 'https://www.youtube.com/watch?v=UM9OK9vFfRM'
                                                   
    copyTube = MyUniTuber(chat_id=chat_id, bot_token=bot_token, filename='NOTCOIN')
    html = await copyTube.get_Tube(url)



# if __name__ == '__main__':
#     logger = logging.getLogger(__name__)#basicConfig(level=logging.INFO, stream=sys.stdout)

#     asyncio.run(main())
