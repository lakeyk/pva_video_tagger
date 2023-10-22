#!/usr/bin/env python

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from frontend import simple_gui

def main():
	simple_gui.create_gui()


if __name__ == "__main__":
	main()
