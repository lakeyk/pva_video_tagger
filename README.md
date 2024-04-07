File: organize_videos.py
Author: Kelsi Lakey (kelsi.lakey@gmail.com, 206-379-6143)
Date: 7/1/21

To Run:
	1. Open a terminal at the location of this file 
		Mac: Right click - open terminal at folder
		Windows: In file explorer, type cmd in file path location and press enter
		Alternatively: Open through applications and navigate to folder
	
	2. Enter the following command into the terminal and press enter. 
	
		python organize_videos.py
		
	3. Use the buttons to load the coaches csv file and the video folder
	
	4. Use the buttons to organize videos and remove audio. 
		Ffmpeg will need to be installed to remove audio.
		For mac, follow the instructions for '2. Static Builds' here: https://superuser.com/questions/624561/install-ffmpeg-on-os-x
		
		
Generating Coaches CSV File
	1. This file should be generated and edited in a text editor.
	Excel can manipulate files in a way that makes them unusable.
	
	2. On each line list the coach followed by their athletes, separated by commas
	
	3. Do not use underscores or spaces to separate first and last name
	
	4. Make sure the names on this list match the labeling
	
Tips / Hints:
	1. Pressing tab after typing o in the terminal with auto fill the script name
	
	2. Pressing up in the terminal will autofill the last command
	
	3. If files are unorganized check spelling and for a spaces at the beginning of the files

	4. If the names match, redo the coaches.csv file in a text editor