#!/usr/local/bin/python3
import subprocess
import shlex
import json
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog
import json
import shlex

root =tk.Tk()
root.withdraw()



# function to find the resolution of the input video file
def findVideoMetada(pathToInputVideo):
    cmd = "ffprobe -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    # prints all the metadata available:
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(ffprobeOutput)

    return ffprobeOutput

#Identify the audio and video streams
def find_streamId(json_object, name):
    a = []
    for dict in json_object["streams"]:
        if dict['codec_type'] == name:
            a.append(dict['index'])
    return a

def afilter(id):
    #8 channel format Example: "[0:0][0:1] [0:2] [0:3] [0:4] [0:5] [0:6] [0:7] amerge=inputs=8"
    #Set Filter String
    a = []
    for i in id:
        a.append("[0:"+str(i)+"] ")
    a_filter = "".join(a)+"amerge=inputs="+str(len(a))
    return a_filter

def fixMultichannel(pathToInputVideo, afilter, saveVideo):
    cmd = "ffmpeg", "-i", pathToInputVideo, "-c:v", "copy", "-c:a","pcm_s16le","-filter_complex", afilter, saveVideo
    subprocess.Popen(cmd)
    return


def mainProgram():
    video_in = filedialog.askopenfilename(title = "Select Video File")
    video_out = filedialog.asksaveasfilename(title = "Save File As", defaultextension=".mov")
    video_dict = findVideoMetada(video_in)
    video_streamId = find_streamId(video_dict, "video")
    audio_streamId = find_streamId(video_dict, "audio")
    amerg_filter = afilter(audio_streamId)

    print(video_in)
    print(amerg_filter)

    fixMultichannel(video_in, amerg_filter, video_out)
    return

mainProgram()



'''
#ffmpeg -i 8trackaudio.mov -filter_complex "[0:0][0:1] [0:2] [0:3] [0:4] [0:5] [0:6] [0:7] amerge=inputs=8" -c:v copy \ -c:a pcm_s16le 8chanaudio.mov
'''
