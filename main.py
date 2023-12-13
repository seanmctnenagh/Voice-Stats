#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains the main function calls for the program. It performs 
    all of the setup actions and then calls the gui() main function."""
# ---------------------------------------------------------------------------
# Imports
import threading                # Contains method to create threads

import data_processing as dp    # Contains data processing functions
from gui import gui, gui_setup  # Contains functions to setup and run the GUI
import audio                    # Contains functions to record and process audio
import input                    # Contains functions to retrieve information from setup.xls

import globals                  # Contains global variables
# ---------------------------------------------------------------------------




if __name__ == "__main__":
    audio.delete_log_files() # Delete all audio files from the audio_files folder

    input.get_info() # Load info from excel file

    gui_setup() # Create GUI Window

    # Create command log
    with open(f"text_files/{globals.match_title}_command_log.txt", "w+") as f:
        f.write("")

    # Start constant audio recording thread
    x = threading.Thread(target=audio.audio_recording, daemon=True)
    x.start()

    # Create dataframes
    dp.create_dataframe()

    # Run main function
    gui()