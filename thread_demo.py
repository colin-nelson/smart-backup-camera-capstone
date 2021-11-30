import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
from threading import Thread
from guizero import App, PushButton, TextBox, Text, Slider
#from GUI import return_offset
import time

#from serial_test import return_distance
import serial
distance = "2"
offset = "0"
def change_offset(slider_value):
    Offset.value = slider_value
    
def increase_offset():
    global offset
    Offset.value = int(Offset.value) + 1
    offset = Offset.value

def decrease_offset():
    global offset
    Offset.value = int(Offset.value) - 1
    offset = Offset.value
#def change_display():
#    Offeset.

def return_offset():
    
    return int(Offset.value)
    
def close_window():
    app.destroy()
    
def getDistance():
    global distance
    global offset
    while True:
        time.sleep(0.1)
        ser = serial.Serial('/dev/ttyACM0', 345600)
        read_serial=ser.readline().decode('utf-8').rstrip()
        
        distance = int(read_serial) - int(offset)
        distance = str(distance)
        #distance = str(read_serial)
        #print(distance)
def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """
    global distance
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    #read_serial=ser.readline()
    #cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
    #    (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    cv2.putText(frame, distance + " mm",
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0),2)
    return frame

def noThreading(source=0):
    """Grab and show video frames without multithreading."""

    cap = cv2.VideoCapture(source)
    cps = CountsPerSec().start()

    while True:
        grabbed, frame = cap.read()
        if not grabbed or cv2.waitKey(1) == ord("q"):
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()
        
def threadVideoGet(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """

    video_getter = VideoGet(source).start()
    cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        cps.increment()

def threadVideoShow(source=0):
    """
    Dedicated thread for showing video frames with VideoShow object.
    Main thread grabs video frames.
    """

    cap = cv2.VideoCapture(source)
    (grabbed, frame) = cap.read()
    video_shower = VideoShow(frame).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed, frame) = cap.read()
        if not grabbed or video_shower.stopped:
            video_shower.stop()
            break

        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()

def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    #Create new distance thread
    dthread = Thread(target=getDistance, args=())
    distance_shower = dthread.start()
    
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        cps.increment()




with open('readme.txt',"r+") as f:
    
        if os.stat("readme.txt").st_size == 0:
            app = App(title ="GUI")
            text = Text(app, text ="Current Offset", size = 40)
            Offset = Text(app, text="0", size = 30)

            pButton = PushButton(app, text = "+", command = increase_offset, align="right")
            mButton = PushButton(app, text = "-", command = decrease_offset, align="left")
            #bSlider = Slider(
            
            exit = PushButton(app, text = "confirm", command = close_window)
            
            
            #offval = int(offset.value)

            app.display() 
             
        else:
            lines = f.readline()
            offset = lines
            print(offset)

        f.write(offset)


f.close()

def main():
    global offset
    
    
   
        
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--thread", "-t", default="none",
        help="Threading mode: get (video read in its own thread),"
            + " show (video show in its own thread), both"
            + " (video read and video show in their own threads),"
            + " none (default--no multithreading)")
    args = vars(ap.parse_args())

    



    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])

    if args["thread"] == "both":
        threadBoth(args["source"])
    elif args["thread"] == "get":
        threadVideoGet(args["source"])
    elif args["thread"] == "show":
        threadVideoShow(args["source"])
    else:
        noThreading(args["source"])

if __name__ == "__main__":
    main()
