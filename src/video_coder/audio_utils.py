import os
from threading import Thread, Lock
import ffmpeg

SUPPORTED_EXTENSIONS = [".mp4", ".MP4", ".MOV", ".mov"]

def remove_audio(videos_path, video_file_name):
	if video_file_name[-4:] in SUPPORTED_EXTENSIONS:
		extension = video_file_name[-4:]
		base_path = os.path.join(videos_path, video_file_name)
		if video_file_name[-10:] == '_audio' + extension:
			video_file_name = video_file_name[:-10] + extension
			os.rename(base_path, os.path.join(videos_path, video_file_name))
			base_path = os.path.join(videos_path, video_file_name)
		video_name = video_file_name[:-4] + '_audio' + extension
		audio_path = os.path.join(videos_path, video_name)
		if os.path.exists(base_path):
			os.rename(base_path, audio_path)
			try:
				input_ffmpeg = ffmpeg.input(audio_path)
				input_video = input_ffmpeg['v']
				ffmpeg.output(input_video, base_path).run()

				lock = Lock()
				with lock:
					if os.path.exists(base_path):
						os.remove(audio_path)
			except Exception as e:
				print('Error removing audio')
				print(e)
				exit()
