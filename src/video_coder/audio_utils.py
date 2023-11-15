import os
from threading import Thread, Lock
import ffmpeg
import moviepy.editor as mp
import speech_recognition as sr

SUPPORTED_EXTENSIONS = [".mp4", ".MP4", ".MOV", ".mov"]
names_dict = {}

# TODO: Move this to a config file
def init_names_dict():
	names_dict["Kelsi"] = ["Kelsi", "Kelsey"]
	names_dict["Tatum"] = ["Tatum"]
	names_dict["Adrian"] = ["Adrian", "Adrieene", "Adrien"]
	names_dict["Ariana"] = ["Ariana", "Arieane", "Arriana"]
	names_dict["Bella"] = ["Bella"]
	names_dict["Boone"] = ["Boone", "Boon", "Boom", "boon", "boom"]
	names_dict["Caman"] = ["Caman", "Canaan", "Cannon"]
	names_dict["Carl"] = ["Carl", "Karl"]
	names_dict["Carter"] = ["Carter", "Karter"]
	names_dict["Charlie"] = ["Charlie"]

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

def autotag_file(videos_path, video_file_name):
	if len(names_dict) == 0:
		init_names_dict()
	r = sr.Recognizer()
	detected = None
	if video_file_name[-4:] not in SUPPORTED_EXTENSIONS:
		return detected
	base_path = os.path.join(videos_path, video_file_name)
	video = mp.VideoFileClip(base_path)
	if video.audio is not None:
		audio_file_name = video_file_name[:-4] + '.wav'
		video.audio.write_audiofile(audio_file_name)
		video.close()
	else:
		video.close()
		return detected

	try:
		with sr.AudioFile(audio_file_name) as source:
			# listen for the data (load audio to memory)
			audio_data = r.record(source)
			# recognize (convert from speech to text)
			text = r.recognize_google(audio_data)
			words = text.split(' ')
			for word in words:
				for name in names_dict:
					if word in names_dict[name]:
						# Rename file with name label if isn't already labeled
						if len(video_file_name) > len(name) and video_file_name[:len(name)] == name:
							detected = 'Already labeled'
							break
						new_file_name = name + '_' + video_file_name
						os.rename(base_path, os.path.join(videos_path, new_file_name))
						detected = name
						break
	except:
		print('Issue running autotagger')
	os.remove(audio_file_name)
	return detected
