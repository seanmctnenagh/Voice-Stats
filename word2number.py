#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains a function to convert numbers in word format into integer format."""
# ---------------------------------------------------------------------------

def word2number(text): # Takes string input and returns int
    numwords = {
        "one" : 1,
        "two" : 2,
        "three" : 3,
        "four" : 4,
        "five" : 5,
        "six" : 6,
        "seven" : 7,
        "eight" : 8,
        "nine" : 9,
        "ten" : 10,
        "eleven" : 11,
        "twelve" : 12,
        "thirteen" : 13,
        "fourteen" : 14,
        "fifteen" : 15,
        "sixteen" : 16,
        "seventeen" : 17,
        "eighteen" : 18,
        "nineteen" : 19,
        "twenty" : 20,
        "twenty one" : 21,
        "twenty two" : 22,
        "twenty three" : 23,
        "twenty four" : 24,
        "twenty five" : 25,
        "twenty six" : 26,
        "twenty seven" : 27,
        "twenty eight" : 28,
        "twenty nine" : 29,
        "thirty" : 30,
        "thirty one" : 31,
        "thirty two" : 32
    }
    try:
        return numwords[text]
    except KeyError: # String not in list of numbers
        return None

if __name__ == "__main__":
    print(word2number("Jake"))