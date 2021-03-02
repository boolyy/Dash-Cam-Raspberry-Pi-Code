import os
import argparse
import cv2
import numpy as np
import sys
import time
from tflite_runtime.interpreter import Interpreter

PROJECT_DIR = os.getcwd()

#String creation of the File Path to the TensorflowLite model and Labels. Change when changing models
PATH_TO_TFLITE = os.path.join(PROJECT_DIR, 'tfModels', 'GoogleSample', 'detect.tflite')
PATH_TO_LABELS = os.path.join(PROJECT_DIR, 'tfModles', 'GoogleSample', 'labelmap.txt')

#Loads the Label Map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

#Meant for the sample Google provides on tensorflow.org
if labels[0] = '???': del(labels[0])

#Change when the EDGE TPU comes to iterpreter = 
# Interpreter(model_path=PATH_TO_CKPT, experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
interpreter = Interpreter(model_path=PATH_TO_TFLITE)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

current_fps = 1
freq = cv2.getTickFrequency()

floating_model = (input_details[0]['dtype'] = np.float32)

input_mean = 127.5
input_std = 127.5

def startRecording():
    date_and_time = time.strftime("%Y-%m-%d-%H:%M") #Stores current date and time in YYYY-MM-DD-HH:MM format
    video_output = 
