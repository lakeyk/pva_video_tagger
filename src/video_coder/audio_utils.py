import os

# This file includes a dependency on ffmpeg

def remove_videos_audio_from_path(path):	
	for r, d, f in os.walk(path):
		for file in f:
			if '.MP4' in file:
				remove_audio(r, file, '.MP4')
			if '.MOV' in file:
				remove_audio(r, file, '.MOV')

def remove_audio(videos_path, video_file_name, extension):
	if video_file_name[-4:] == extension:
		base_path = os.path.join(videos_path, video_file_name)
		if video_file_name[-10:] == '_audio' + extension:
			video_file_name = video_file_name[:-10] + extension
			os.rename(base_path, os.path.join(videos_path, video_file_name))
			base_path = os.path.join(videos_path, video_file_name)
		video_name = video_file_name[:-4] + '_audio' + extension
		audio_path = os.path.join(videos_path, video_name)
		if os.path.exists(base_path):
			os.rename(base_path, audio_path)
			ffmpeg_command = 'ffmpeg -i \"' + audio_path + '\" -vcodec copy -an \"' + base_path + '\"'
			print(ffmpeg_command)
			os.system(ffmpeg_command)
			if os.path.exists(base_path):
				os.remove(audio_path)
