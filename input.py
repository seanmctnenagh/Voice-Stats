#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions for loading the information from the setup.xls
    file into the relevant globals variables."""
# ---------------------------------------------------------------------------
# Imports
import contextlib       # Contains method to supress errors by type
import pandas as pd     # Used to read the excel sheets
import math             # Contains functions to test if variable is NaN

import globals
# ---------------------------------------------------------------------------
def get_info():
    """ Main function of the file. Reads the excel sheet, removes blank names and NaN numbers and 
    applies the values to the global variables"""

    setup = pd.read_excel('setup.xls', sheet_name="Setup")  # Read sheet data
    team_0 = pd.read_excel('setup.xls', sheet_name="Team 1")
    team_1 = pd.read_excel('setup.xls', sheet_name="Team 2")

    globals.match_title = setup[1][0]       # Set Match Title
    globals.half_length = int(setup[1][1])  # Set Half Length
    globals.team_names[0] = team_0[1][2]    # Set Team 0 name
    globals.team_names[1] = team_1[1][2]    # Set Team 1 name

    team0_players, team1_players = get_players(team_0, team_1) # Retrieve player names

    team0_numbers, team1_numbers = get_numbers(team_0, team_1) # Retrieve player numbers

    team0_players, team1_players, team0_numbers, team1_numbers = remove_blanks(team0_players, team1_players, team0_numbers, team1_numbers)

    globals.event_names = get_events(setup) # Retrieve event names

    team0_players, team1_players = no_name(team0_players, team1_players) # Sets players with no name to have name ""

    globals.team0_players = team0_players # Set Team 0 names
    globals.team1_players = team1_players # Set Team 1 names

    globals.team0_numbers = [int(number) for number in team0_numbers] # Set Team 0 numbers
    globals.team1_numbers = [int(number) for number in team1_numbers] # Set Team 1 numbers

def no_name(team0_players, team1_players):
    """If a player has a number but no name, set name to """""
    for i, _ in enumerate(team0_players): 
        with contextlib.suppress(TypeError):
            if math.isnan(team0_players[i]):
                team0_players[i] = ""
    for i, _ in enumerate(team1_players):
        with contextlib.suppress(TypeError):
            if math.isnan(team1_players[i]):
                team1_players[i] = ""
    return team0_players, team1_players

def remove_blanks(team0_players, team1_players, team0_numbers, team1_numbers):
    """Remove blanks values from the player names and numbers"""
    for i in reversed(range(len(team0_players))): 
        if team0_players[i] in ['', 'nan'] and math.isnan(team0_numbers[i]):
            team0_numbers.pop(i)
            team0_players.pop(i)
        if team1_players[i] in ['', 'nan'] and math.isnan(team1_numbers[i]):
            team1_numbers.pop(i)
            team1_players.pop(i)
    return team0_players, team1_players, team0_numbers, team1_numbers


def get_players(team_0, team_1): 
    """Retrieve the player names from the cells in the excel sheet"""
    try:
        team_0 = [team_0[3][4], team_0[1][8], team_0[3][8], team_0[5][8], team_0[1][12], team_0[3][12], team_0[5][12], team_0[2][16], team_0[4][16], team_0[1][20], team_0[3][20], team_0[5][20], team_0[1][24], team_0[3][24], team_0[5][24], team_0[0][27], team_0[1][27], team_0[2][27], team_0[3][27], team_0[4][27], team_0[5][27], team_0[6][27], team_0[0][30], team_0[1][30], team_0[2][30], team_0[3][30], team_0[4][30], team_0[5][30], team_0[6][30], team_0[0][33], team_0[1][33], team_0[2][33], team_0[3][33], team_0[4][33], team_0[5][33], team_0[6][33]]
    except KeyError: # If no names in last row of sheet, row is not imported and KeyError occurs
        team_0 = [team_0[3][4], team_0[1][8], team_0[3][8], team_0[5][8], team_0[1][12], team_0[3][12], team_0[5][12], team_0[2][16], team_0[4][16], team_0[1][20], team_0[3][20], team_0[5][20], team_0[1][24], team_0[3][24], team_0[5][24], team_0[0][27], team_0[1][27], team_0[2][27], team_0[3][27], team_0[4][27], team_0[5][27], team_0[6][27], team_0[0][30], team_0[1][30], team_0[2][30], team_0[3][30], team_0[4][30], team_0[5][30], team_0[6][30], '', '', '', '', '', '', '']
    
    try:
        team_1 = [team_1[3][4], team_1[1][8], team_1[3][8], team_1[5][8], team_1[1][12], team_1[3][12], team_1[5][12], team_1[2][16], team_1[4][16], team_1[1][20], team_1[3][20], team_1[5][20], team_1[1][24], team_1[3][24], team_1[5][24], team_1[0][27], team_1[1][27], team_1[2][27], team_1[3][27], team_1[4][27], team_1[5][27], team_1[6][27], team_1[0][30], team_1[1][30], team_1[2][30], team_1[3][30], team_1[4][30], team_1[5][30], team_1[6][30], team_1[0][33], team_1[1][33], team_1[2][33], team_1[3][33], team_1[4][33], team_1[5][33], team_1[6][33]]
    except KeyError: # If no names in last row of sheet, row is not imported and KeyError occurs
        team_1 = [team_1[3][4], team_1[1][8], team_1[3][8], team_1[5][8], team_1[1][12], team_1[3][12], team_1[5][12], team_1[2][16], team_1[4][16], team_1[1][20], team_1[3][20], team_1[5][20], team_1[1][24], team_1[3][24], team_1[5][24], team_1[0][27], team_1[1][27], team_1[2][27], team_1[3][27], team_1[4][27], team_1[5][27], team_1[6][27], team_1[0][30], team_1[1][30], team_1[2][30], team_1[3][30], team_1[4][30], team_1[5][30], team_1[6][30], '', '', '', '', '', '', '']
    
    return team_0, team_1

def get_numbers(team_0, team_1): 
    """Retrieve the player numbers from the cells in the excel sheet"""
    team_0 = [team_0[3][3], team_0[1][7], team_0[3][7], team_0[5][7], team_0[1][11], team_0[3][11], team_0[5][11], team_0[2][15], team_0[4][15], team_0[1][19], team_0[3][19], team_0[5][19], team_0[1][23], team_0[3][23], team_0[5][23], team_0[0][26], team_0[1][26], team_0[2][26], team_0[3][26], team_0[4][26], team_0[5][26], team_0[6][26], team_0[0][29], team_0[1][29], team_0[2][29], team_0[3][29], team_0[4][29], team_0[5][29], team_0[6][29], team_0[0][32], team_0[1][32], team_0[2][32], team_0[3][32], team_0[4][32], team_0[5][32], team_0[6][32]]
    team_1 = [team_1[3][3], team_1[1][7], team_1[3][7], team_1[5][7], team_1[1][11], team_1[3][11], team_1[5][11], team_1[2][15], team_1[4][15], team_1[1][19], team_1[3][19], team_1[5][19], team_1[1][23], team_1[3][23], team_1[5][23], team_1[0][26], team_1[1][26], team_1[2][26], team_1[3][26], team_1[4][26], team_1[5][26], team_1[6][26], team_1[0][29], team_1[1][29], team_1[2][29], team_1[3][29], team_1[4][29], team_1[5][29], team_1[6][29], team_1[0][32], team_1[1][32], team_1[2][32], team_1[3][32], team_1[4][32], team_1[5][32], team_1[6][32]]

    return team_0, team_1

def get_events(setup):
    """Retrieve the event names from the cells in the excel sheet"""
    return [event for event in setup[3].values if type(event) == str]
