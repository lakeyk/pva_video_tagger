import os
from threading import Thread, Lock
import ffmpeg
import moviepy.editor as mp
import speech_recognition as sr
from video_coder import names_helper as names

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
				ffmpeg_command = 'ffmpeg -i \"' + audio_path + '\" -vcodec copy -an \"' + base_path + '\"'
				os.system(ffmpeg_command)

				lock = Lock()
				with lock:
					if os.path.exists(base_path):
						os.remove(audio_path)
			except Exception as e:
				print('Error removing audio')
				print(e)
				exit()

def autotag_file(videos_path, video_file_name):
	names_dict = names.get_names_dict()
	r = sr.Recognizer()
	detected = None
	text = None
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
		return text, detected

	try:
		with sr.AudioFile(audio_file_name) as source:
			# listen for the data (load audio to memory)
			audio_data = r.record(source)
			# recognize (convert from speech to text)
			text = r.recognize_google(audio_data)
			words = text.split(' ')
			for i in range(len(words)):
				word = words[i]
				if i + 1 < len(words) and words[i+1] in names.INITIALS:
					word = word + ' ' + words[i+1]
				for name in names_dict:
					if word in names_dict[name]:
						# Rename file with name label if isn't already labeled
						if len(video_file_name) > len(name) and video_file_name[:len(name)] == name:
							detected = 'Already labeled'
							break
						new_file_name = name + '_day5_'
						if "GS" in text or "DS" in text or "Diaz" in text or "yes" in text:
							new_file_name = new_file_name + 'GS_'
						if "Slalom" in text or "slalom" in text or "salon" in text or "swallower" in text or "song" in text or "Sloan" in text:
							new_file_name = new_file_name + 'SL_'
						if "run 2" in text or "Run 2" in text or "Run two" in text or "run two" in text or "run to" in text:
							new_file_name = new_file_name + 'run2_'
						if "run 1" in text or "Run 1" in text or "Run one" in text or "run one" in text or "run won" in text:
							new_file_name = new_file_name + 'run1_'
						new_file_name = new_file_name + video_file_name
						os.rename(base_path, os.path.join(videos_path, new_file_name))
						detected = name
						break
	except Exception as e:
		print('Issue running autotagger')
		print(e)
	os.remove(audio_file_name)
	return text, detected
