#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to export the match data to a local folder."""
# ---------------------------------------------------------------------------

# Imports
import seaborn as sb                # Functions to create heatmaps
import matplotlib.pyplot as plt     # Functions to plot figures
import os                           # Functions to control the OS
import shutil                       # Functions to copy files
from datetime import date           # Function to get today's date
import PySimpleGUI as sg            # Functions to run the GUI
import contextlib                   # Functions to supress errors
import pandas as pd                 # Functions to create dataframes and read excel sheets
from PIL import Image               # Functions to alter images

from drawing import redraw_figure   # Function to redraw the figure on the canvas

import globals                      # Globals variables

# ---------------------------------------------------------------------------

def save_heatmaps(path):
    dataframe = globals.df0
    scaled_dataframe = (dataframe - dataframe.min(axis=0))/(dataframe.max(axis=0) - dataframe.min(axis=0)) # scale data in each column to between 0 and 1
    scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
    heatmap = sb.heatmap(scaled_dataframe[:15], cmap="Blues", robust=True,
                    linewidth=0.3,cbar=False, annot=dataframe[:15]) # Put scaled data into heatmap with non scaled data as annotations
    plt.tick_params(axis='both', which='major',
                    labelbottom = False, bottom=False, top = False, labeltop=True) # Set tick labels parameters
    plt.yticks(rotation=0) # Rotate labels
    heatmap = heatmap.get_figure()    
    heatmap.savefig(f'{path}/{globals.team_names[0]}.png', dpi=400)

    dataframe = globals.df1
    scaled_dataframe = (dataframe - dataframe.min(axis=0))/(dataframe.max(axis=0) - dataframe.min(axis=0)) # scale data in each column to between 0 and 1
    scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
    heatmap = sb.heatmap(scaled_dataframe[:15], cmap="Blues", robust=True,
                    linewidth=0.3,cbar=False, annot=dataframe[:15]) # Put scaled data into heatmap with non scaled data as annotations
    plt.tick_params(axis='both', which='major',
                    labelbottom = False, bottom=False, top = False, labeltop=True) # Set tick labels parameters
    plt.yticks(rotation=0) # Rotate labels
    heatmap = heatmap.get_figure()    
    heatmap.savefig(f'{path}/{globals.team_names[1]}.png', dpi=400)

    dataframe = globals.df
    scaled_dataframe = dataframe.div(dataframe.max(axis=1), axis=0) # scale data in each row to between 0 and 1
    scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
    heatmap = sb.heatmap(scaled_dataframe, cmap="Blues", robust=True,
                linewidth=0.3,cbar=False, annot=dataframe) # Put scaled data into heatmap with non scaled data as annotations
    plt.tick_params(axis='both', which='major',
                    labelbottom = False, bottom=False, top = False, labeltop=True) # Set tick labels parameters
    plt.yticks(rotation=0) # Rotate labels
    heatmap = heatmap.get_figure()    
    heatmap.savefig(f'{path}/Team Totals.png', dpi=400)

    redraw_figure()
    crop_image(f'{path}/Team Totals.png')


def export_data(): # Export dataframes to excel
    today = date.today().strftime("%d-%m-%Y")

    path = f'{os.getcwd()}/Match Reports/{globals.match_title} {globals.team_names[0]} vs {globals.team_names[1]} {today}'

    with contextlib.suppress(FileExistsError):
        os.mkdir(path) # Create folder to hold exported data and command log
    file = f'{path}/{globals.match_title} {globals.team_names[0]} vs {globals.team_names[1]} {today}.xlsx'

    # Copy command log to export folder
    shutil.copyfile(f"text_files/{globals.match_title}_command_log.txt", f"{path}/{globals.match_title}_command_log.txt")

    save_heatmaps(path)

    try:
        with pd.ExcelWriter(file) as writer: # Write excel sheets
            globals.df.to_excel(writer, sheet_name='Team Totals')
            globals.df0.to_excel(writer, sheet_name=globals.team_names[0])
            globals.df1.to_excel(writer, sheet_name=globals.team_names[1])
    except PermissionError:
        sg.popup("Close File and Try Again")
        return

    #Popup to confirm export
    sg.popup_no_buttons("\nData Exported\n", keep_on_top=True,auto_close=True,icon=None, auto_close_duration=2, no_titlebar=True)

def crop_image(path):
    # Opens an image in RGB mode
    im = Image.open(path)
    
    # Size of the image in pixels
    width, height = im.size
    
    # Setting the points for cropped image
    left = 0
    top = 0
    right = width
    bottom = height - 140
    
    # Cropped image of above dimension
    im1 = im.crop((left, top, right, bottom))

    im1.save(path)