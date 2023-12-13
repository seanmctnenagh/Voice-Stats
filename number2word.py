#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains a function to convert numbers in int format into word format."""

import contextlib
# ---------------------------------------------------------------------------

def number2word(number): # Takes int or list of ints input and returns string or list of strings
    if type(number) == list: # if list
        return [number2word(num) for num in number]

    with contextlib.suppress(ValueError):
        number = int(number)
    if type(number) != int: # if not int
        return None

    number = number

    numwords = {
        1: 'one', 
        2: 'two', 
        3: 'three', 
        4: 'four', 
        5: 'five', 
        6: 'six', 
        7: 'seven', 
        8: 'eight', 
        9: 'nine', 
        10: 'ten', 
        11: 'eleven', 
        12: 'twelve', 
        13: 'thirteen', 
        14: 'fourteen', 
        15: 'fifteen', 
        16: 'sixteen', 
        17: 'seventeen', 
        18: 'eighteen', 
        19: 'nineteen', 
        20: 'twenty', 
        21: 'twenty one', 
        22: 'twenty two', 
        23: 'twenty three', 
        24: 'twenty four', 
        25: 'twenty five', 
        26: 'twenty six', 
        27: 'twenty seven', 
        28: 'twenty eight', 
        29: 'twenty nine', 
        30: 'thirty', 
        31: 'thirty one', 
        32: 'thirty two'}

    try:
        return numwords[number]
    except KeyError: # Number not in list
        return None
