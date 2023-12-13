#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to create and run the GUI window."""
# ---------------------------------------------------------------------------
# Imports
import threading                # Contains method to create threads
import PySimpleGUI as sg        # Functions to run the GUI
from datetime import datetime   # Functions to get current time
from os import listdir, remove  # Functions to find and delete files
from os.path import isfile, join# Functions to check files and combine strings into a path

import drawing                  # Functions to draw the figure on the GUI canvas
import export                   # Functions to export the match data

import globals                  # Contains global variables
# ---------------------------------------------------------------------------

def gui_setup():
    w, h = get_w_h()
    image_col = [[sg.Image(r'images/recording.png', key='-REC-')]] # Load recording notification image

    # Define the window's contents i.e. layout
    data_col = [ # Column with navigation buttons and canvas
        [   sg.Push(),
            sg.Column(image_col, element_justification='c'),
            sg.Push(),
            sg.Button('Team Totals',enable_events=True, key='-TOTALS-', font='Helvetica 16', expand_x=True),
            sg.Button(globals.team_names[0],enable_events=True, key='-TEAM0-', font='Helvetica 16', expand_x=True),
            sg.Button(globals.team_names[1],enable_events=True, key='-TEAM1-', font='Helvetica 16', expand_x=True),
            sg.Button('Export Data',enable_events=True, key='-EXPORT-', font='Helvetica 16', expand_x=True),
            sg.Button('Start Match',enable_events=True, key='-TIMING-', font='Helvetica 16', expand_x=True),
            sg.Push()],
        [sg.Push(), sg.Text("", font=('calibri',25), justification='center', auto_size_text=True, key='-TITLE-'),sg.Push()],
        [sg.Push(), sg.Canvas(key='-CANVAS-', pad=(20,20)), sg.Push()]
    ]
    com_feed = [
        [sg.Multiline("", key="-FEED-", text_color='black', background_color='white', size=(190, h-45), autoscroll=True)]
    ]
    com_feed_col = [ # Column with command feed and clock
        [sg.Text('00:00', key='-TIME-', font='System 18', background_color='red', expand_y=True)],
        [sg.Text("Command Feed", font=('calibri',19), justification='center', auto_size_text=True)],
        [sg.Frame("",com_feed, size=(200,h-35), background_color='white', title_color='black', border_width=0, title_location='n')]]

    data_layout = [ # combine columns
        [sg.Push(),sg.Column(data_col, element_justification='c'), sg.Column(com_feed_col, element_justification='c'),sg.Push()]
        ]

    # Create window
    globals.window = sg.Window('Stats Tracker', data_layout, resizable = True, finalize=True, return_keyboard_events=True)
    globals.window.Maximize()

    # Set window title
    title = "Team Totals"
    globals.window['-TITLE-'].update(title)

    globals.window['-REC-'].update(visible=False)

def get_w_h():
    blank = sg.Window("",layout=[], alpha_channel=0) # Create a blank window
    w, h = blank.get_screen_size() # Use blank window to get screen height and width
    blank.close() # Close blank window
    return w, h

def gui():
    # Draw figure on canvas
    drawing.redraw_figure()

    while True:
        event, _ = globals.window.read(timeout=3000) # Read window for events and timeout after 3 seconds
        match event:
            case " ": # Recording button
                if not globals.start_recording:
                    globals.start_recording = True
                    globals.window['-REC-'].update(visible=True)
                elif not globals.end_recording:
                    globals.end_recording = True
                    globals.window['-REC-'].update(visible=False)
            case '__TIMEOUT__': # Window read timeout after 3 seconds
                pass
            case sg.WIN_CLOSED:
                files = [f for f in listdir('text_files') if isfile(join('text_files', f))]
                for file in files:
                    remove(f'text_files/{file}')
                exit()
            case '-TOTALS-': # Team totals button, change view to team totals
                title = "Team Totals"
                globals.window['-TITLE-'].update(title)
                globals.view = globals.views[0]
            case '-TEAM0-': # Team 0 button, change view to team 0
                title = globals.team_names[0]
                globals.window['-TITLE-'].update(title)
                globals.view = globals.views[1]
            case '-TEAM1-': # Team 1 button, change view to team 1
                title = globals.team_names[1]
                globals.window['-TITLE-'].update(title)
                globals.view = globals.views[2]
            case '-TIMING-': # Timing button, updates latest timing action
                if not globals.start_match: # Start Match
                    globals.start_match = True
                    globals.window['-TIME-'].Widget.configure(background='green')
                    globals.window['-TIMING-'].update("Half Time")
                    now = datetime.now()
                    globals.start_hour = now.hour
                    globals.start_minute = now.minute
                    globals.start_second = now.second
                    d = threading.Thread(target=drawing.run_clock, daemon=True)
                    d.start()
                elif not globals.half_time_begin: # Half Time
                    globals.window['-TIME-'].Widget.configure(background='red')
                    globals.window['-TIMING-'].update("Start Second Half")
                    globals.half_time_begin = True
                elif not globals.half_time_end: # Start Second Half
                    globals.window['-TIME-'].Widget.configure(background='green')
                    globals.window['-TIMING-'].update("Full Time")
                    globals.half_time_end = True
                    now = datetime.now()
                    globals.second_half_hour = now.hour
                    globals.second_half_minute = now.minute
                    globals.second_half_second = now.second
                else: # Full Time
                    globals.full_time = True
                    globals.window['-TIME-'].Widget.configure(background='red')
                    globals.window['-TIMING-'].update(disabled=True)
            case '-EXPORT-': # Export Data button
                export.export_data()
            case _:
                continue
            
        drawing.redraw_figure() # Redraw figure on canvas
        b = threading.Thread(target=drawing.comm_feed, daemon=True) # New thread to update command feed
        b.start()