#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to create and update the dataframes and plot the heatmaps."""
# ---------------------------------------------------------------------------

# Imports
import numpy as np              # Functions to create arrays
import pandas as pd             # Functions to create dataframes
import matplotlib.pyplot as plt # Functinos to plot figures
import seaborn as sb            # Functions to create heatmap tables

import globals                  # Global variables             
# ---------------------------------------------------------------------------

def create_dataframe():
    ## Create arrays of zeroes
    teams_data = np.zeros((len(globals.event_names), 2))
    teams_data = np.array(teams_data,dtype=int)

    team0_data = np.zeros((len(globals.team0_numbers),len(globals.event_names)))
    team0_data = np.array(team0_data,dtype=int)

    team1_data = np.zeros((len(globals.team1_numbers),len(globals.event_names)))
    team1_data = np.array(team1_data,dtype=int)

    ## Turn arrays into dataframes

    globals.df = pd.DataFrame(teams_data, index = globals.event_names, columns=globals.team_names)

    globals.df0 = pd.DataFrame(team0_data, index=[f'{globals.team0_players[i]} {globals.team0_numbers[i]}' for i in range(len(globals.team0_numbers))], columns=globals.event_names)

    globals.df1 = pd.DataFrame(team1_data, index=[f'{globals.team1_players[i]} {globals.team1_numbers[i]}' for i in range(len(globals.team1_numbers))], columns=globals.event_names)

# Update function
def update_data(event, team, player):
    if player != "Unknown":
        if team == globals.team_names[0]: # Update team dataframe
            globals.df0[event][player] += 1
        elif team == globals.team_names[1]:
            globals.df1[event][player] += 1

    globals.df[team][event] += 1 # Update totals dataframe

def plot_data():  

    fig = plt.figure(figsize=(11, 9)) # Create a figure

    if globals.view== globals.views[0]: # Team Totals
        dataframe = globals.df
        scaled_dataframe = dataframe.div(dataframe.max(axis=1), axis=0) # scale data in each row to between 0 and 1
        scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
        sb.heatmap(scaled_dataframe, cmap="Blues", robust=True,
                    linewidth=0.3,cbar=False, annot=dataframe) # Put scaled data into heatmap with non scaled data as annotations
    
    elif globals.view== globals.views[1]: # Team 1
        dataframe = globals.df0
        scaled_dataframe = (dataframe - dataframe.min(axis=0))/(dataframe.max(axis=0) - dataframe.min(axis=0))  # scale data in each column to between 0 and 1
        scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
        sb.heatmap(scaled_dataframe[:15], cmap="Blues", robust=True,
                    linewidth=0.3,cbar=False, annot=dataframe[:15]) # Put scaled data into heatmap with non scaled data as annotations
    
    elif globals.view== globals.views[2]: # Team 2
        dataframe = globals.df1
        scaled_dataframe = (dataframe - dataframe.min(axis=0))/(dataframe.max(axis=0) - dataframe.min(axis=0)) # scale data in each column to between 0 and 1
        scaled_dataframe.fillna(0, inplace=True) # Scaling turns 0s to NaNs so replace those with 0s
        sb.heatmap(scaled_dataframe[:15], cmap="Blues", robust=True,
                    linewidth=0.3,cbar=False, annot=dataframe[:15]) # Put scaled data into heatmap with non scaled data as annotations


    plt.tick_params(axis='both', which='major',
                    labelbottom = False, bottom=False, top = False, labeltop=True) # Set tick labels parameters
    plt.yticks(rotation=0) # Rotate labels
    return fig

def undo_command():
    event, team, player = globals.commands[len(globals.commands)-1] # Get last command
    print(f'{event=}')
    globals.commands.pop()

    if event == "Sub":
        sub_command(team, player)
        return
    elif player == "Unknown":
        pass
    elif team == globals.team_names[0]: # subtract from dataframe
        globals.df0[event][player] -= 1
    elif team == globals.team_names[1]: # subtract from dataframe
        globals.df1[event][player] -= 1

    globals.df[team][event] -= 1 # subtract from dataframe


def sub_command(team, players):
    if team == globals.team_names[0]:
        index_list = [f'{globals.team0_players[i]} {globals.team0_numbers[i]}' for i in range(len(globals.team0_numbers))]
        a, b = index_list.index(players[0]), index_list.index(players[1])
        index_list[b], index_list[a] = index_list[a], index_list[b]
        globals.team0_players[b], globals.team0_players[a] = globals.team0_players[a], globals.team0_players[b]
        globals.team0_numbers[b], globals.team0_numbers[a] = globals.team0_numbers[a], globals.team0_numbers[b]
        globals.df0 = globals.df0.reindex(index_list, axis="index")
    elif team == globals.team_names[1]:
        index_list = [f'{globals.team1_players[i]} {globals.team1_numbers[i]}' for i in range(len(globals.team1_numbers))]
        a, b = index_list.index(players[0]), index_list.index(players[1])
        index_list[b], index_list[a] = index_list[a], index_list[b]
        globals.team1_players[b], globals.team1_players[a] = globals.team1_players[a], globals.team1_players[b]
        globals.team1_numbers[b], globals.team1_numbers[a] = globals.team1_numbers[a], globals.team1_numbers[b]
        globals.df1 = globals.df1.reindex(index_list, axis="index")
