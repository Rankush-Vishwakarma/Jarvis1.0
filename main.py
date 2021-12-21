import subprocess
import shlex
import time
import Jarvis_01
import signal
import os
from Jarvis_01 import speak
import ast
import math
process1 = subprocess.Popen('pythonw detectEmotion.py > emotion_output.txt &', stdout=subprocess.PIPE, shell=True)
print('emotion detection process has been runned')
#stdout = process1.communicate()
# Poll process.stdout to show stdout live
time.sleep(25)
#print('process 2 going to run')
process2 = subprocess.run(['python','Jarvis_01.py'], shell = True)
print('Jarvis has been stopped')
subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process1.pid))
# fetching the emotion dictionary
file = open('emotion_output.txt','r').readlines()
def Max_min_average(emotion_detected):
    max_emotion = max(zip(emotion_detected.values(), emotion_detected.keys()))[1]
    average_length = math.ceil(sum(emotion_detected for emotion_detected in emotion_detected.values() ) / len(emotion_detected))
    min_emotions = [key for key, value in emotion_detected.items() if value < average_length]
    mean_emotion = [key for key, value in emotion_detected.items() if value == average_length]
    second_emotion = [key for key,value in emotion_detected.items() if value == sorted(emotion_detected.values())[-2]]
    return max_emotion,mean_emotion,min_emotions,second_emotion
def tell_emotion(emotion_detected):
    max_emotion,mean_emotion,min_emotion,second_emotion = Max_min_average(emotion_detected)
    speak(f'sir you are very {max_emotion} today also having {second_emotion[0]} second highest emotion and I can see you have {min_emotion} as the minimum one  ')


if __name__ == '__main__':
    if len(file) != 0:
        emotion_detected = ast.literal_eval(file[-1])
        tell_emotion(emotion_detected)
    else:
        speak('no emotion detected')
