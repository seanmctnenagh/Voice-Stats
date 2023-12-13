#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Author  : Seán McTiernan
# ---------------------------------------------------------------------------
""" This file contains functions to record and process audio and to delete log files."""
# ---------------------------------------------------------------------------

# Imports
import wave                     # Functions to parse wave files
import speech_recognition as sr # Function to call Google Speech Recognition API
import pyaudio
import threading                # Method to create threads
from os import listdir, remove  # Functions to find and delete files
from os.path import isfile, join# Functions to check files and combine strings into a path
import winsound                 # Function to play system sounds

from parse import parse
import data_processing as dp    # Data processing functions

import globals                  # Global variables             
# ---------------------------------------------------------------------------

chunk=3024
channels=2
rate=44100
audio=pyaudio.PyAudio()

def delete_log_files(): # delete all audio files
    files = [f for f in listdir('audio_files') if isfile(join('audio_files', f))]
    for file in files:
        remove(f'audio_files/{file}')


def process_audio(path): # pass audio file to recognizer, pass text to parser, pass commands to data updater
    r = sr.Recognizer()
    audio_file = sr.AudioFile(path)

    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    text = r.recognize_google(audio, show_all=True)

    event, team, player = parse(text)

    if "Undo" in [event, team, player]:
        dp.undo_command()
        return

    if event == "Sub":
        dp.sub_command(team, player)
        return

    if None in [event, team, player]:
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        remove(path)
        return

    dp.update_data(event, team, player)


def audio_recording(): # Constantly record audio, save to file when flag set
    frames = []
    i=0
    while True:
        stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=3024)
        while not globals.start_recording: # can take some time from space pressed to flag being set so it grabs the previous few seconds of audio
            data = stream.read(chunk*50)
            frames = [data]
        while not globals.end_recording: # when recording flag set
            data = stream.read(chunk)
            frames.append(data)
        globals.end_recording = False # reset flags
        globals.start_recording = False

        stream.close()

        ## Save file

        file = f'audio_files/phrase{i}.wav'

        wf = wave.open(file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        z = threading.Thread(target=process_audio, args=(file,), daemon=True)
        z.start()
        i += 1