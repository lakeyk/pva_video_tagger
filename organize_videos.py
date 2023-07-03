"""
athlete_name_dict []:
    key = labeling name
    value = full name

Looking up video match:
    file name
    remove appending _, .
    get athlete name from labeling name (athlete_name_dict)
    
How do we define labeling name?

CSV:
    full name     Optional(labeling name)
"""

#!/usr/bin/env python

import csv 
import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#from dropboxSync import DropboxSync
#from pathlib import Path

def main():
	global athlete_name_dict
	athlete_name_dict = {}
	
	global path
	path = "\\"
	global unorganized_path
	global duplicates_path
	
	global athletes_video_list
	athletes_video_list = []
	
	create_gui()
			
def parse_csv(file_path):	
	# Open and parse CSV file
	csvfile = open(file_path)
	for row in csvfile.readlines()[1:]:
		row = row.rstrip('\n')
		array = row.split(',')
		if len(array) < 1:
			print('row: ' + str(row) + ' formatted incorrectly, len= ' + str(len(array)))
			return
		athlete_full_name = array[0]
		if len(array) < 2: # Use the first name as the label name.
			athlete_name = athlete_full_name.split()
			athlete_label_name = athlete_name[0]
		else:
			athlete_label_name = array[1]
		athlete_name_dict[athlete_label_name.strip()] = athlete_full_name.strip()

def organize_by_athletes():
	add_info_text("\nOrganizing by Athletes:\n")
	get_videos_from_path("athletes")
	update_tree_display()
	check_for_all_athletes()
	check_if_files_organized()

def check_for_all_athletes():
	for athlete in athlete_name_dict:
		if athlete not in athletes_video_list:
			add_info_text('\tWARNING: No videos found for ' + athlete + '\n')

def check_if_files_organized():
	organized = True
	if os.path.exists(unorganized_path):
		dirs = os.listdir(unorganized_path)
		organized = False
		if len(dirs) == 1:
			add_info_text('\nWARNING: ' + str(len(dirs)) + ' video left to move, check Unorganized folder\n')
		else:
			add_info_text('\nWARNING: ' + str(len(dirs)) + ' videos left to move, check Unorganized folder\n')
	if os.path.exists(duplicates_path):
		dirs = os.listdir(duplicates_path)
		organized = False
		if len(dirs) == 1:
			add_info_text('\nWARNING: ' + str(len(dirs)) + ' potential duplicate, check Duplicates folder\n')
		else:
			add_info_text('\nWARNING: ' + str(len(dirs)) + ' potential duplicates, check Duplicates folder\n')
	if organized:
		add_info_text('\nAll videos successfully organized!\n')
			
def get_videos_from_path(parsing):
	# Move video files
	for r, d, f in os.walk(path):
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
	for dirpath, _, _ in os.walk(path, topdown=False):
		if dirpath == path:
			break
		try:
			os.rmdir(dirpath)
		except OSError as ex:
			# This is ok
			pass

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
	base_path = os.path.join(videos_path, video_file_name)
	athletename = None
	if athlete_label_name in athlete_name_dict:
		athletename = athlete_name_dict[athlete_label_name]
		if athlete_label_name not in athletes_video_list:
			athletes_video_list.append(athlete_label_name)
		new_path = get_athletes_path(path, athletename, video_file_name)
		
		if os.path.exists(base_path):
			if os.path.exists(new_path) and not os.path.samefile(new_path, base_path):
				print(new_path)
				if not os.path.exists(duplicates_path):
					os.makedirs(duplicates_path)
				os.rename(base_path, os.path.join(duplicates_path, video_file_name))
			else:
				os.rename(base_path, new_path)	
	else:		
		if not os.path.exists(unorganized_path):
			os.makedirs(unorganized_path)
		if os.path.exists(base_path):
			os.rename(base_path, os.path.join(unorganized_path, video_file_name))
    

def remove_audio_command():
	add_info_text("\nRemoving Audio, Please Wait...\n")
	window.after(1000, lambda:remove_videos_audio_from_path())
	
def remove_videos_audio_from_path():	
	for r, d, f in os.walk(path):
		for file in f:
			if '.MP4' in file:
				remove_audio(r, file, '.MP4')
			if '.MOV' in file:
				remove_audio(r, file, '.MOV')
	add_info_text("\nAll Audio Has Been Removed!\n")

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

def open_folder_dialog():
	path_directory = filedialog.askdirectory(initialdir = "\\", title = "Select Video Folder")
	print(path_directory)
	#path_directory = path_directory.replace('/','\\')
	print(path_directory)
	if len(path_directory) > 0:
		global path
		path = path_directory
		update_paths()
		update_tree_display()
		video_folder_text.configure(state='normal')
		video_folder_text.insert(1.0, path)
		video_folder_text.configure(state='disabled')

def open_file_dialog():
	# TODO(lakeyk): Update open location to code directory.
	path_file = filedialog.askopenfilename(initialdir = "\\", title = "Select Athletes Name File", filetypes = [("csv files","*.csv")])
	if len(path_file) > 0:
		parse_csv(path_file)
		athletes_file_text.configure(state='normal')
		athletes_file_text.insert(1.0, path_file)
		athletes_file_text.configure(state='disabled')
		
def update_paths():
	global unorganized_path
	global duplicates_path
	unorganized_path = os.path.join(path, 'Unorganized')
	duplicates_path = os.path.join(path, 'Duplicates')

def create_gui():
	global window
	window = tk.Tk()
	greeting = tk.Label(text='PVA Video Tagger', font = ('', 20))
	greeting.grid(row = 0, column = 0, columnspan = 3, pady = 10)
    
	athletes_file_label = tk.Label(text='Athletes Name File', font = ('', 12))
	athletes_file_label.grid(row = 2, column = 0, pady = 10)
    
	global athletes_file_text
	athletes_file_text = tk.Text(window, height = 1, bg = "white")
	athletes_file_text.grid(row = 2, column = 1, pady = 10)
	athletes_file_text.configure(state='disabled')
    
	athletes_file_button = tk.Button(
		text="Select",
		width = 15,
		height = 1,
		bg = "blue",
        fg="yellow",
		command = open_file_dialog
	)
	athletes_file_button.grid(row = 2, column = 2)

	video_folder_label = tk.Label(text='Video Folder', font = ('', 12))
	video_folder_label.grid(row = 3, column = 0, pady = 10)

	global video_folder_text
	video_folder_text = tk.Text(window, height = 1, bg = "white")
	video_folder_text.grid(row = 3, column = 1, pady = 10)
	video_folder_text.configure(state='disabled')
    
	path_button = tk.Button(
		text="Select",
		width = 15,
		height = 1,
		bg = "blue",
        fg="yellow",
		command = open_folder_dialog
	)
	path_button.grid(row = 3, column = 2, padx=20)
	
	remove_audio_button = tk.Button(
		text="Remove Audio",
		width=15,
		height=1,
		bg="blue",
		fg="yellow",
		command = remove_audio_command
	)
	remove_audio_button.grid(row = 5, column = 1, padx = 10)
	
	organize_by_athletes_button = tk.Button(
		text="Sort",
		width=15,
		height=1,
		bg="blue",
		fg="yellow",
		command = organize_by_athletes
	)
	organize_by_athletes_button.grid(row=5, column=0, padx = 20)
	
	global tree
	tree = ttk.Treeview()#height = 15)
	global root_node
	tree.grid(row = 6, column = 0, columnspan = 3, pady = 15, padx = 20, sticky=tk.NSEW)
	
	global info_text
	info_text = tk.Text(window, height = 15, bg = "light gray")
	info_text.grid(row = 9, column = 0, columnspan = 3, pady = 10, padx = 20, sticky=tk.NSEW)
	scrollb = tk.Scrollbar(window, command = info_text.yview)
	#scrollb.grid(row = 9, column = 3, sticky = 'nsew', pady = 10)
	info_text['yscrollcommand'] = scrollb.set
	
	window.mainloop()
	
def add_info_text(comment):
	info_text.configure(state='normal')
	info_text.insert(tk.END, comment)
	info_text.see(tk.END)
	info_text.configure(state='disabled')
	
def update_tree_display():
	tree.delete(*tree.get_children())
	root_node = tree.insert('', 'end', text=path, open=True)
	process_directory(root_node, path)	

def process_directory(parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            if not p.startswith('.'):
            	oid = tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                process_directory(oid, abspath)

if __name__ == "__main__":
	main()
