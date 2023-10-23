import os
import ffmpeg

def remove_videos_audio_from_path(path):	
	for r, d, f in os.walk(path):
		for file in f:
			print(file)
			if '.MP4' or '.mp4' in file:
				remove_audio(r, file, '.MP4')
			if '.MOV' or '.mov' in file:
				remove_audio(r, file, '.MOV')

def remove_audio(videos_path, video_file_name, extension):
	if video_file_name[-4:].upper() == extension:
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
			except:
				print('Error removing audio')
				exit()
			if os.path.exists(base_path):
				os.remove(audio_path)
