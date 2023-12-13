#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains the globals variables needed by the program.
    They contain sample values so that the program can be used without setup.xls"""
# ---------------------------------------------------------------------------

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
team0_players = [""]*32
team1_players = [""]*32

# Lists of player numbers
team0_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
team1_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# List of event names
event_names = ["goal","point","wide","tackle", "block", "free conceded", "save"] 

# List of team names
team_names = ["A", "Roscrea"]
team_nicknames = ["Blues", "Reds"]

# Match Title
match_title = "Munster Final"

# List of views for canvas
views = ["Team Totals", team_names[0], team_names[1]]

# Set default view
view = views[0]

# Holds latest command for undo function
commands = []

# GUI window so that it can be accessed from all files and threads
window = None

# Recording flags shared between threads
start_recording = False
end_recording = False

# Figure on canvas
fig_agg = None

# Dataframes
df, df0, df1 = None, None, None

# half Length
half_length = 30

# Time of match start
start_hour = 0
start_minute = 0
start_second = 0

# Time of second half start
second_half_hour = 0
second_half_minute = 0
second_half_second = 0

# Flags for time events
start_match = False
half_time_begin = False
half_time_end = False
full_time = False
