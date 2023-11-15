#simple_gui

import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import glob
from video_coder import file_utils, audio_utils
from threading import Thread, Lock

def get_video_files(path):
	video_files = []
	for r, d, f in os.walk(path):
		for file in f:
			extension = None
			if file[-4:] in audio_utils.SUPPORTED_EXTENSIONS:
				video_files.append((r, file))
	return video_files

def remove_videos_audio_from_path(path):
	add_text(info_text, "\nRemoving Audio, Please Wait...\n\n")

	video_files = get_video_files(path)

	file_count = len(video_files)
	add_text(info_text, f"Removing audio from {file_count} files\n")
	for i in range(file_count):
		add_text(info_text, f"{i+1}/{file_count}: {video_files[i][0]}/{video_files[i][1]}\n")
		audio_utils.remove_audio(video_files[i][0], video_files[i][1])

	add_text(info_text, "\nAll Audio Has Been Removed!\n")

def remove_audio_command():
    path = video_folder_text.get("1.0", tk.END).rstrip('\n')
    thread = Thread(target=lambda: remove_videos_audio_from_path(path))
    thread.start()

def run_auto_tagger_on_path(path):
	add_text(info_text, "\nRunning auto-tagger, Please Wait...\n\n")
	video_files = get_video_files(path)

	file_count = len(video_files)
	add_text(info_text, f"Auto-tagging {file_count} files\n")
	for i in range(file_count):
		add_text(info_text, f"{i+1}/{file_count}: {video_files[i][0]}/{video_files[i][1]}\n")
		result = audio_utils.autotag_file(video_files[i][0], video_files[i][1])
		add_text(info_text, f"\tAuto-tagged as: {result}\n")

	add_text(info_text, "\nAuto-tagger complete for all files!\n")

def auto_tag_command():
    path = video_folder_text.get("1.0", tk.END).rstrip('\n')
    thread = Thread(target=lambda: run_auto_tagger_on_path(path))
    thread.start()

def open_folder_dialog():
	path_directory = filedialog.askdirectory(initialdir = "\\", title = "Select Video Folder")
	print(path_directory)
	#path_directory = path_directory.replace('/','\\')
	print(path_directory)
	if len(path_directory) > 0:
		file_utils.update_paths(path_directory)
		update_video_tree_display(path_directory)
		video_folder_text.configure(state='normal')
		video_folder_text.delete(1.0, tk.END)
		video_folder_text.insert(1.0, path_directory)
		video_folder_text.configure(state='disabled')

def open_file_dialog():
	base_path = os.path.abspath(os.path.dirname(__file__))
	file_path = filedialog.askopenfilename(initialdir = base_path, title = "Select Athletes Name File", filetypes = [("text file","*.txt")])
	load_athletes_file(file_path)
	
def load_athletes_file(file_path):
	if len(file_path) > 0:
		athletes_name_dict = file_utils.parse_file(file_path)
		add_athletes_to_tree(athletes_name_dict)
		athletes_file_text.configure(state='normal')
		athletes_file_text.delete(1.0, tk.END)
		athletes_file_text.insert(1.0, file_path)
		athletes_file_text.configure(state='disabled')

def autoload_athletes_file():
	# Search for latest txt file in current directory
	crnt_dir = os.path.abspath(os.path.dirname(__file__))
	config_dir = os.path.join(crnt_dir, "..\..\..\config")
	try:
		files = list(filter(os.path.isfile, glob.glob(config_dir + "\*")))
		files.sort(key=os.path.getctime)
		for p in reversed(files):
			if not os.path.isdir(p) and p.endswith('.txt') and 'athletes' in p:
				load_athletes_file(p)
	except:
		print('Could not load directory: ' + crnt_dir)

def create_gui():
	global window
	window = tk.Tk()
	greeting = tk.Label(text='PVA Video Tagger', font = ('', 20))
	greeting.grid(row = 0, column = 0, columnspan = 5, pady = 10)
    
	athletes_file_label = tk.Label(text='Athletes Name File', font = ('', 12))
	athletes_file_label.grid(row = 2, column = 0, pady = 10)
    
	global athletes_file_text
	athletes_file_text = tk.Text(window, height = 1, bg = "white")
	athletes_file_text.grid(row = 2, column = 1, columnspan = 2, pady = 10)
	athletes_file_text.configure(state='disabled')
    
	athletes_file_button = tk.Button(
		text="Select",
		width = 15,
		height = 1,
		bg = "gray",
	        fg="black",
		command = open_file_dialog
	)
	athletes_file_button.grid(row = 2, column = 3)

	video_folder_label = tk.Label(text='Video Folder', font = ('', 12))
	video_folder_label.grid(row = 3, column = 0, pady = 10)

	global video_folder_text
	video_folder_text = tk.Text(window, height = 1, bg = "white")
	video_folder_text.grid(row = 3, column = 1, columnspan = 2, pady = 10)
	video_folder_text.configure(state='disabled')
    
	path_button = tk.Button(
		text="Select",
		width = 15,
		height = 1,
		bg = "gray",
        	fg="black",
		command = open_folder_dialog
	)
	path_button.grid(row = 3, column = 3, padx=20)

	edit_athletes_button = tk.Button(
		text="Edit Athletes",
		width=15,
		height=1,
		bg="gray",
		fg="black",
		command = edit_athletes
	)
	edit_athletes_button.grid(row = 7, column = 0, padx = 10)
    
	remove_audio_button = tk.Button(
		text="Remove Audio",
		width=15,
		height=1,
		bg="gray",
		fg="black",
		command=lambda: remove_audio_command()
	)
	remove_audio_button.grid(row = 7, column = 3, padx = 10)
	
	organize_by_athletes_button = tk.Button(
		text="Sort",
		width=15,
		height=1,
		bg="gray",
		fg="black",
		command = organize_by_athletes
	)
	organize_by_athletes_button.grid(row=7, column=2, padx = 20)

	auto_tag_button = tk.Button(
		text="AutoTag",
		width=15,
		height=1,
		bg="gray",
		fg="black",
		command = lambda: auto_tag_command()
	)
	auto_tag_button.grid(row=7, column=1, padx = 20)
	
	global athletes_tree
	athletes_tree = ttk.Treeview()
	global athletes_root_node
	autoload_athletes_file()
	athletes_tree.grid(row = 6, column = 0, columnspan = 1, pady = 15, padx = 20, sticky=tk.NSEW)

	global video_tree
	video_tree = ttk.Treeview()
	global video_root_node
	video_tree.grid(row = 6, column = 1, columnspan = 3, pady = 15, padx = 20, sticky=tk.NSEW)
	
	global info_text
	info_text = tk.Text(window, height = 15, bg = "light gray")
	info_text.grid(row = 9, column = 0, columnspan = 4, pady = 10, padx = 20, sticky=tk.NSEW)
	scrollb = tk.Scrollbar(window, command = info_text.yview)
	info_text['yscrollcommand'] = scrollb.set
	
	window.mainloop()

def process_directory(parent, path):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        isdir = os.path.isdir(abspath)
        if not p.startswith('.'):
            oid = video_tree.insert(parent, 'end', text=p, open=False)
        if isdir:
            process_directory(oid, abspath)

def update_video_tree_display(path):
	video_tree.delete(*video_tree.get_children())
	video_root_node = video_tree.insert('', 'end', text=path, open=True)
	process_directory(video_root_node, path)

def add_athletes_to_tree(athlete_name_dict):
	athletes_tree.delete(*athletes_tree.get_children())
	athletes_root_node = athletes_tree.insert('', 'end', text='Full Name, Label Name', open=True)
	for athlete in athlete_name_dict:
		athletes_tree.insert(athletes_root_node, 'end', text=athlete_name_dict[athlete] + ', ' + athlete, open=False)

def add_text(text_box, comment, disable = True):
	text_box.configure(state='normal')
	text_box.insert(tk.END, comment)
	text_box.see(tk.END)
	if disable:
		text_box.configure(state='disabled')

def save_athletes_command(top, text_box):
	text = text_box.get('1.0', tk.END).splitlines()
	for line in text:
		add_text(info_text, line + '\n')
	athletes_name_dict = file_utils.save_athletes(text)
	add_athletes_to_tree(athletes_name_dict)
	file_utils.write_athlets_to_csv(athletes_file_text.get("1.0", tk.END))
	top.destroy()

def edit_athletes():
	top = tk.Toplevel(window)
	top.geometry("750x250")
	top.title("Athletes List")
	athletes_edit_text = tk.Text(top, height = 10, bg = "light gray")
	athletes_edit_text.grid(row = 0, column = 0, columnspan = 3, pady = 10, padx = 20, sticky=tk.NSEW)
	scrollb = tk.Scrollbar(top, command = athletes_edit_text.yview)
	athletes_edit_text['yscrollcommand'] = scrollb.set
	save_button = tk.Button(
        top,
		text="Save",
		width=15,
		height=1,
		bg="gray",
		fg="black",
		command = lambda: save_athletes_command(top, athletes_edit_text)
	)
	save_button.grid(row=1, column=2, padx = 20)
	athlete_name_dict = file_utils.get_athlete_name_dict() 
	for athlete in athlete_name_dict:
		add_text(athletes_edit_text, athlete_name_dict[athlete] + ', ' + athlete + '\n', False)

def organize_by_athletes():
	add_text(info_text, "\nOrganizing by Athletes:\n")
	file_utils.get_videos_from_path("athletes")
	update_video_tree_display(video_folder_text.get("1.0", tk.END).rstrip('\n'))
	missing_athletes = file_utils.get_missing_athletes()
	for athlete in missing_athletes:
		add_text(info_text, '\tWARNING: No videos found for ' + athlete + '\n')
	organized = True
	if file_utils.check_if_unorganized():
		add_text(info_text, '\nWARNING: Videos left to move, check Unorganized folder\n')
		organized = False
	if file_utils.check_if_duplicates():
		add_text(info_text, '\nWARNING: Potential duplicates, check Duplicates folder\n')
		organized = False
	if organized:
		add_text(info_text, '\nAll videos successfully organized!\n')
