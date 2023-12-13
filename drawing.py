#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to draw, redraw and delete figures on the canvas.
    Also to run the clock and update the command feed."""
# ---------------------------------------------------------------------------

# Imports
import time                                     # Function to perform sleeps
from datetime import datetime                   # Functions to find the current time
import matplotlib.pyplot as plt                 # Functions to plot figures
# Class to combine figure and canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     
import data_processing as dp                    # Contains data processing functions

import globals                                  # Global variables             
# ---------------------------------------------------------------------------

def draw_figure(canvas, figure): # Draw figure on canvas
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='left', fill='both', expand=1)
        globals.fig_agg = figure_canvas_agg

def delete_fig_agg(): # Delete figure from canvas
    globals.fig_agg.get_tk_widget().forget()
    plt.close('all')

def redraw_figure():
    if globals.fig_agg is not None: # Delete current figure
        delete_fig_agg()
    figure = dp.plot_data() # Plot new figure
    if figure is None:
        return
    canvas_elem = globals.window['-CANVAS-'].TKCanvas # Find canvas
    draw_figure(canvas_elem, figure) # Draw figure on canvas

def run_clock(): # Constantly running function for clock
    while not globals.half_time_begin: # Check for half time
        time.sleep(0.8) # Sleep so as to not run unnecessary loops

        ## Find time
        now = datetime.now()
        minutes = ((now.hour - globals.start_hour) * 60) + (now.minute - globals.start_minute)
        seconds = now.second - globals.start_second
        if seconds < 0:
                minutes -= 1
                seconds = 60 + seconds
        globals.window['-TIME-'].update(f'{minutes:02d}:{seconds:02d}') # Update clock with time string

    while not globals.half_time_end: # During half time
        globals.window['-TIME-'].update(f'{globals.half_length}:00') # Set clock to start of second half time
        time.sleep(2) # Sleep while waiting to start second half

    while not globals.full_time: # During second half
        time.sleep(0.8) # Sleep to prevent uncessary looping

        ## Find time
        now = datetime.now()
        minutes = ((now.hour - globals.second_half_hour) * 60) + (now.minute - globals.second_half_minute) + globals.half_length
        seconds = now.second - globals.second_half_second
        if seconds < 0:
                minutes -= 1
                seconds = 60 + seconds
        globals.window['-TIME-'].update(f'{minutes:02d}:{seconds:02d}') # Print time string to clock

    
def comm_feed(): # Add command from log to on screen feed
    with open(f"text_files/{globals.match_title}_command_log.txt", "r+") as text:
        globals.window['-FEED-'].update(text.read())
