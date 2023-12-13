#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to compare strings that are not an exact match."""
# ---------------------------------------------------------------------------

# Imports
from thefuzz import fuzz         # Function to find comparison ratio between strings
import itertools                 # Functions to combine loops       

# ---------------------------------------------------------------------------

def fuzzy(choices, text, strict=False):
    choices = clean_choices(choices) # Removes empty strings and sorts list
    
    pairs, triples = create_pairs_triples(text) # Create pairs and triples of words
    
    input_text = format_input(text) # Split input into single words and remove duplicates

    results_80, results_60, results_49 = perform_fuzzy(choices, input_text, strict, pairs, triples)

    try:
        if results_80.count(max(results_80)) == 1: # If single most >80% accuracies, return that value
            return choices[results_80.index(max(results_80))]
        elif results_60.count(max(results_60)) == 1: # If single most >60% accuracies, return that value
            return choices[results_60.index(max(results_60))]
        elif results_49.count(max(results_49)) == 1: # If single most >50% accuracies, return that value
            return choices[results_49.index(max(results_49))]
        else:
            return None
    except ValueError:
        return None

def perform_fuzzy(choices, input_text, strict, pairs, triples):
    results_80 = [0]*len(choices) # Hold number of times each choice had an accuracy of over 80%
    results_60 = [0]*len(choices) # Hold number of times each choice had an accuracy of over 60%
    results_49 = [0]*len(choices) # Hold number of times each choice had an accuracy of over 50%
    for i, choice in enumerate(choices): # Iterate through events/teams/players
        if len(str(choice).split(" ")) == 1: # If single word choice
            words = input_text
        elif len(str(choice).split(" ")) == 2: # If 2 word choice
            words = pairs
        elif len(str(choice).split(" ")) == 3: # If 3 word choice
            words = triples
        for word in words: # Iterate through input words/pairs/triples
            ratio = fuzz.ratio(word.lower(), str(choice).lower()) # Get comparison score
            if ratio > 80: # If > 80%, add 1 to 80% list
                results_80[i] += 1
            if not strict: # If strict, only scores above 80% are counted
                if ratio > 60: # If > 60%, add 1 to 60% list
                    results_60[i] += 1
                elif ratio > 49: # If > 49%, add 1 to 49% list
                    results_49[i] += 1
    return results_80, results_60, results_49

def format_input(text):
    input_text=[] # Hold list of words input
    for phrase in text: # Split incoming phrases into list of words
        input_text.extend(iter(phrase.split()))
    # input_text = list(dict.fromkeys(input_text)) # Remove duplicates from list of words
    return input_text

def clean_choices(choices):
    choices = [choice for choice in choices.copy() if choice != '']
    choices = list(filter(None, choices))
    try:
        choices.sort() # sort list of events/team names/players
    except TypeError:
        print(choices)
    return choices

def create_pairs_triples(text):
    pairs = [word_groups(item, 2) for item in text]
    pairs = [item for sublist in pairs for item in sublist]
    triples = [word_groups(item, 3) for item in text]
    triples = [item for sublist in triples for item in sublist]
    return pairs,triples


def word_groups(words, number): # Creates a list of pairs, triples etc. of words
    groups = []
    for j in range(len(words.split())-(number-1)):
        group = ""
        for i in range(number):
            if words.split()[j + i] != " ":
                group += words.split()[j+i]
                if i < number-1 and group != '':
                    group += " "
                else:
                    break
        if group not in ['', ' ', '  ']:
            groups.append(group)
    return groups

def fuzzy_remove(text, result):
    if type(result) == list: # Recursion
        for item in result:
            text = fuzzy_remove(text, item)
        return text
    result = str(result)

    if len(result.split(" ")) == 1:
        for i, phrase in enumerate(text):
            words = phrase.split(" ")
            for word in words:
                if fuzz.ratio(word.lower(), result.lower()) > 60:
                    text[i] = phrase.replace(f" {word}", '')
                    text[i] = text[i].replace(word, '')
    elif len(result.split(" ")) == 2:
        for i, phrase in enumerate(text):
            pairs = word_groups(phrase, 2)
            for pair in pairs:
                if fuzz.ratio(pair.lower(), result.lower()) > 60:
                    text[i] = text[i].replace(f" {pair}", "")
                    text[i] = text[i].replace(pair, "")
    elif len(result.split(" ")) == 3:
        for i, phrase in enumerate(text):
            triples = word_groups(phrase, 3)
            for triple in triples:
                if fuzz.ratio(triple.lower(), result.lower()) > 60:
                    text[i] = text[i].replace(f" {triple}", "")
                    text[i] = text[i].replace(triple,)

    return text

def exact_check(choices, text):
    choices = list(filter(None, choices)) # remove empty strings
    for phrase, choice in itertools.product(text, choices): # Loop through choices and phrases
        if type(choice) != int:
            if choice.lower() in [word.lower() for word in word_groups(phrase, len(choice.split()))]:
                return choice
        elif str(choice) in phrase.split():
            return choice
    return None