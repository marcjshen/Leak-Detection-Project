#!/usr/bin/python3
import pyaudio
import wave
import datetime
import time
import os

# From Script 2:
from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np
import glob
#import os
import RPi.GPIO as GPIO
#import time
#import pyaudio
#import wave
import sounddevice as sd
import soundfile as sf
#import ConfigParser
import RPi.GPIO as GPIO
import requests
import json

# DEFAULTS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 8192
RECORD_SECONDS = 10
RECORD_PERIODS = 4
FINAL_LEAKS = 4
TARGET_DIR = "/Desktop/home/pi/"
API_KEY = 'o.F6iN9x3T5spuMqBgaIbKCcuWDAxk1DFj'

def pushMessage(title, body):
    data = {

        'type':'note',

        'title':title,

        'body:body  }
    resp = requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(API_KEY, ''))

def record_audio(format, channels, rate, seconds, framers_per_buffer):
    """
    Records audio for a set number of seconds, and saves it to the output directory
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, 
                        channels=channels, 
                        rate=rate,
                        input=True,
                        framers_per_buffer=frames_per_buffer)

    # Start recording
    print("recording")
    frames = []
    for i in range(0, int(rate / frames_per_buffer * seconds)):
        data = stream.read(frames_per_buffer, exception_on_overflow = False)
        frames.append(data)
        
    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("stop recording")

    # Get name and location of file to create
    filename = "/home/pi/Desktop/myfile.wave"
    # write data to audio file
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

def bucketifyMedian(data, buckets=24000):
    """
    Given a list of numbers, compresses it into a number of equal length 'buckets'
    calculated by taking the median of data within the bucket ranges
    """
    size = len(data) // buckets
    bucketed_data = []
    for bucket in range(buckets):
        median_buckets = np.median(data[bucket*size+size])
        bucketed_data.append(median_buckets)
    return bucketed_data

def readFileToFFT(f):
    """
    Given an audio filename, reads the data and performs a fast fourier transform
    (FFT) on the data
    """
    sample_rate, data = wavefile.read(f)
    data = fft(data)
    data = abs(data)
    data = data[0:int(len(data)/2)]
    return data

def evalFFTMedianData(data, threshold=.1, data_range=[3500,6500]):
    """
    Given a list of fft data of length 24000, evaluates whether the data represents
    a leak by summing the data within a range, comparing it to the total sum of the
    data, and returning whether or not the smaller sum is above a certain threshold
    percent of the larger sum.
    """
    total_amplitude_sum = sum(data)
    data_range_amplitude_sum = sum(data[data_range[0]:data_range[1]])
    percent_in_range = data_range_amplitude_sum * 1.0 / total_amplitude_sum
    return percent_in_range > threshold

def evalFile(filename):
    """
    Evaluates whether or not a given audio file indicates a leak
    """
    fft_data = readFileToFFT(filename)
    median_buckets = bucketifyMedian(fft_data)
    running_water = evalFFTMedianData(median_buckets)
    return running_water

record_counter = 0
leak_counter = 0

def leakperhour(leak):
    """
    Given a boolean indicating whether or not there is a leak, adds to a leak_counter
    """
    if leak:
        #GPIO.output(19,GPIO.HIGH)
        #GPIO.output(13,GPIO.LOW)
        global leak_counter
        leak_counter += 1
        print("leak")
        #time.sleep(1)
    else:
        #GPIO.output(LEAK_PIN,GPIO.LOW)
        #GPIO.output(NO_LEAK_PIN,GPIO.HIGH)
        print('No leak')

def sendalert(leak_found):
    """
    Given a boolean indicating whether or not there is a leak, sends alert if there is
    """
    if leak_found:
        #GPIO.output(19,GPIO.HIGH)
        #GPIO.output(13,GPIO.LOW)
        pushMessage("Leak!", "Please check on grate #1")
        print('Leak sent')
    else:
        pushMessage("No leak", "No leak detected in grate #1")
        print('No leak sent')

while True:
    record_counter = 0
    leak_counter = 0
    for i in range(RECORD_PERIODS):
        # Record audio
        record_counter += 1
        record_audio(FORMAT, CHANNELS, RATE, RECORD_SECONDS, CHUNK)
        
        # Run analysis on audio
        leakperhour(evalFile("/home/pi/Desktop/myfile.wav"))
        print(leak_counter)
        time.sleep(5)
    sendalert(leak_counter == record_counter)
        # something to send a message to FE&P