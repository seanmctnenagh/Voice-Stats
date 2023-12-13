#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to find the event, team and player in the input text."""
# ---------------------------------------------------------------------------

# Imports
import contextlib                               # Function to supress errors
import itertools                                # Functions to combine loops
# Functions to check and remove close and exact string matches
from fuzzy import fuzzy, fuzzy_remove, exact_check 
# Class to combine figure and canvas
from number2word import number2word as n2w      # Function to convert numbers to words
from word2number import word2number as w2n      # Function to convert words to numbers

import globals                                  # Global variables             
# ---------------------------------------------------------------------------

def clean_input(text): # This function removes common filler words that are not used to determine the event and will only slow down and confuse the parser
    mapping = [ ('/', ' '), ('-', ' '), (' a ', ' '), (' an ', ' '), (' by ', ' '), (' for ', ' '), (' scored ', ' '), ('subtle', 'sub'), (' number ', ' '), ('that\'s', ' '), ('there\'s', ' '), ('that', ' '), ('there', ' '), ('go4kora', ''), ('pt4', 'point'), ('three conceded', 'free conceded'), ('3 conceded', 'free conceded'), ('3 considered', 'free conceded'), ('three considered', 'free conceded'), ('point four', 'point'), ('point 4', 'point'), ('goal 4', 'goal'), ('goal four', 'goal') ]
    for (i, _), (k, v) in itertools.product(enumerate(text), mapping):
        text[i] = text[i].replace(k, v)

    return text

def check_undo(text): # This function checks if the event is "Undo"
    words = ['undo', 'undone']
    if fuzzy(words, text, True) in words:
        return True

def check_sub(text):
    words = ['sub', 'substitution']
    if fuzzy(words, text, True) in words:
        return True

def unknown(text):
    words = ['unknown', 'Un known']
    if fuzzy(words, text, True) in words:
        return True

def write(command="", undo=False): # Write command to log
    if not undo:
        with open(f"text_files/{globals.match_title}_command_log.txt","a+") as f:
            with contextlib.suppress(TypeError):
                if globals.commands == []:
                    f.write(f'{globals.window["-TIME-"].DisplayText}: {command}\n')
                else:
                    f.write(f'\n{globals.window["-TIME-"].DisplayText}: {command}\n')
    else:
        with open(f"text_files/{globals.match_title}_command_log.txt", 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.truncate()
            f.writelines(lines[:-2])

def check_team(text):
    team = exact_check(globals.team_names, text)
    if team is None:
        team = fuzzy(globals.team_names.copy(), text, strict=True) # Find team
        if team is None:
            team = exact_check(globals.team_nicknames, text)
            if team is None:
                team = fuzzy(globals.team_nicknames.copy(), text, strict=True) # Find team
                if team is None:
                    return None, text

    text = fuzzy_remove(text, team) # Remove team name from input
    if team in globals.team_nicknames:
        team = globals.team_names[globals.team_nicknames.index(team)]
    return team, text

def check_event(text):
    event = exact_check(globals.event_names, text)
    if event is None:
        event = fuzzy(globals.event_names.copy(), text) # Find event
    if event is None:
        return None, text
    text = fuzzy_remove(text, event)
    return event, text

def check_player(text, team):
    if check_keeper(text):
        player = combine_name_number(team, "1")
        text = fuzzy_remove(text, ["keeper", "goalie", "goalkeeper"])
        return player, text

    if unknown(text):
        return ("Unknown", text)
    if team == globals.team_names[0]:
        player = exact_check(globals.team0_players+[str(number) for number in globals.team0_numbers]+n2w(globals.team0_numbers), text)
        if player is None:
            player = fuzzy(globals.team0_players.copy()+[str(number) for number in globals.team0_numbers]+n2w(globals.team0_numbers), text)
    elif team == globals.team_names[1]:
        player = exact_check(globals.team1_players+[str(number) for number in globals.team1_numbers]+n2w(globals.team1_numbers), text)
        if player is None:
            player = fuzzy(globals.team1_players.copy()+[str(number) for number in globals.team1_numbers]+n2w(globals.team1_numbers), text)
    if player is None:
        return (player, text)
    text = fuzzy_remove(text, player)
    if w2n(player) is not None:
        text = fuzzy_remove(text, w2n(player))
    if n2w(player) is not None:
        text = fuzzy_remove(text, n2w(player))

    player = combine_name_number(team, player)

    return (player, text)
    
def check_keeper(text):
    words = ['keeper', 'goalie', 'goalkeeper']
    if fuzzy(words, text, True) in words:
        return True

def player_check_without_team(text):
    player = exact_check(globals.team0_players, text)
    team = None
    if player is None:
        player = exact_check(globals.team1_players, text)
    else:
        team = globals.team_names[0]
        return combine_name_number(team, player), team, fuzzy_remove(text, player)
    
    if player is None:
        player = fuzzy(globals.team0_players.copy(), text)
    else:
        team = globals.team_names[1]
        return combine_name_number(team, player), team, fuzzy_remove(text, player)
    
    if player is None:
        player = fuzzy(globals.team1_players.copy(), text)
    else:
        team = globals.team_names[0]
        return combine_name_number(team, player), team, fuzzy_remove(text, player)

    if player is not None:
        team = globals.team_names[1]

    return combine_name_number(team, player), team, fuzzy_remove(text, player)

def sub(text):
    text = fuzzy_remove(text, ["sub", "substitution"])
    team, text = check_team(text)
    player_1, text = check_player(text, team)
    player_2, text = check_player(text, team)
    if None in [team, player_1, player_2]:
        return None, None, None
    write(f'Sub {team.capitalize()} {player_1} for {player_2}') # Write to command log
    globals.commands.append(["Sub", team, [player_1, player_2]])
    return "Sub", team, [player_1, player_2]

def parse(text):
    try:
        text = [phrase['transcript'] for phrase in text['alternative']] # Split predictions into a list

    except: 
        pass
        # return None, None, None

    print(text)

    text = clean_input(text) # remove filler words

    if check_undo(text): # Check if undo command entered
        write(undo=True)
        return "Undo", "Undo", "Undo"

    if check_sub(text):
        return sub(text)

    team, text = check_team(text)
    if team is None:
        player, team, text = player_check_without_team(text)
    if team is None:
        return None, None, None

    event, text = check_event(text)
    if event is None:
        return None, None, None

    if 'player' not in locals():
        player, text = check_player(text, team)
    if player is None:
        return None, None, None
        
    write(f'{event.capitalize()} {team.capitalize()} {player}') # Write to command log

    globals.commands.append([event, team, player]) # Add command to list of commands

    return event, team, player

def combine_name_number(team, player):
    if w2n(player) is not None:
        player = w2n(player)
    if team == globals.team_names[0]:
        if player in globals.team0_players: # If player found by name
            index = globals.team0_players.index(player) # Get index of player in team list
        elif int(player) in globals.team0_numbers: # If player found by number
            index = globals.team0_numbers.index(int(player)) # Get index of player in team list
        player = f'{globals.team0_players[index]} {globals.team0_numbers[index]}' # Combine player name and number

    elif team == globals.team_names[1]:
        if player in globals.team1_players: # If player found by name
            index = globals.team1_players.index(player) # Get index of player in team list
        elif int(player) in globals.team1_numbers: # If player found by number
            index = globals.team1_numbers.index(int(player)) # Get index of player in team list
        player = f'{globals.team1_players[index]} {globals.team1_numbers[index]}' # Combine player name and number
    return player
