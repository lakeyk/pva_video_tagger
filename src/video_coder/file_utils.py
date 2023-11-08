import os
import time
import glob

athlete_name_dict = {}
athletes_video_list = []

def add_athlete_row(row):
	row = row.rstrip('\n')
	array = row.split(',')
	if len(array) < 1 or len(array[0]) < 1:
		print('row: ' + str(row) + ' formatted incorrectly, athlete not added')
		return
	athlete_full_name = array[0]
	if len(array) < 2: # Use the first name as the label name.
		athlete_name = athlete_full_name.split()
		athlete_label_name = athlete_name[0]
	else:
		athlete_label_name = array[1]
	athlete_name_dict[athlete_label_name.strip()] = athlete_full_name.strip()    

def parse_file(file_path):
	# Open and parse athletes file
	print(file_path)
	athlete_name_dict.clear()
	file = open(file_path)
	for row in file.readlines()[1:]:
		add_athlete_row(row)
	return athlete_name_dict

def get_videos_from_path(parsing):
	# Move video files
	for r, d, f in os.walk(base_path):
		for file in f:
			if '_audio.MP4' in file:
				new_file_name = file[0:-10] + '.MP4'
				os.rename(os.path.join(r, file), os.path.join(r, new_file_name))
			if '.MP4' in file:
				move_video_file(r, file, parsing)
			if '_audio.MOV' in file:
				new_file_name = file[0:-10] + '.MOV'
				os.rename(os.path.join(r, file), os.path.join(r, new_file_name))
			if '.MOV' in file:
				move_video_file(r, file, parsing)
			
	# Delete empty folders	
	for dirpath, _, _ in os.walk(base_path, topdown=False):
		if dirpath == base_path:
			break
		try:
			os.rmdir(dirpath)
		except OSError as ex:
			# This is ok
			pass

def get_missing_athletes():
	missing_athletes = []
	for athlete in athlete_name_dict:
		if athlete not in athletes_video_list:
			missing_athletes.append(athlete)
	return missing_athletes

def check_if_unorganized():
	if os.path.exists(unorganized_path):
		return True
	return False

def check_if_duplicates():
	if os.path.exists(duplicates_path):
		return True
	return False

def get_athletes_path(path, athletename, video_file_name):
	athletes_path = os.path.join(path, 'athletes')
	athletes_path = os.path.join(athletes_path, athletename)
		
	# Create folders
	if not os.path.exists(athletes_path):
		os.makedirs(athletes_path)
				
	new_path = os.path.join(athletes_path, video_file_name)
	
	return new_path
	
def move_video_file(videos_path, video_file_name, parsing):
	athlete_label_name = video_file_name
	for i in range (0, len(video_file_name)):
		if video_file_name[i] == '.' or video_file_name[i] == '_':
			athlete_label_name = video_file_name[0:i]
			break
	video_base_path = os.path.join(videos_path, video_file_name)
	athletename = None
	if athlete_label_name in athlete_name_dict:
		athletename = athlete_name_dict[athlete_label_name]
		if athlete_label_name not in athletes_video_list:
			athletes_video_list.append(athlete_label_name)
		new_path = get_athletes_path(base_path, athletename, video_file_name)
		
		if os.path.exists(video_base_path):
			if os.path.exists(new_path) and not os.path.samefile(new_path, video_base_path):
				print(new_path)
				if not os.path.exists(duplicates_path):
					os.makedirs(duplicates_path)
				os.rename(video_base_path, os.path.join(duplicates_path, video_file_name))
			else:
				os.rename(video_base_path, new_path)	
	else:		
		if not os.path.exists(unorganized_path):
			os.makedirs(unorganized_path)
		if os.path.exists(video_base_path):
			os.rename(video_base_path, os.path.join(unorganized_path, video_file_name))

def update_paths(path):
	global unorganized_path
	global duplicates_path
	global base_path
	base_path = path
	unorganized_path = os.path.join(path, 'Unorganized')
	duplicates_path = os.path.join(path, 'Duplicates')

def write_athlets_to_csv(path):
    updated_file_path = path.split('.txt')[0] + '_' + str(int(time.time())) + '.txt'
    file = open(updated_file_path, "w")
    file.write("Athlete Name, Label Name\n")
    for athlete in athlete_name_dict:
        file.write(athlete_name_dict[athlete] + ', ' + athlete + '\n')
    file.close()

def save_athletes(text):
	athlete_name_dict.clear()
	for line in text:
		add_athlete_row(line)
	return athlete_name_dict

def get_athlete_name_dict():
	return athlete_name_dict
