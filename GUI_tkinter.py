from tkinter import *
from PIL import ImageTk, Image
#from GUI import return_offset
from serial_test import return_distance
from cv2 import *


root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.grid()
# Create a label in the frame
lmain = Label(app)
lmain.grid()

# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    overlay(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    #imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)
    
    #overlay(frame)

def get_distance():
    #offset = return_offset()
    distance = return_distance()
    #distance -= offset
    return str(distance)

def overlay(frame):
    d = get_distance() + "mm"
    #d = str(10)
    font  = cv2.FONT_HERSHEY_SIMPLEX
    #InputOutputArray img, const String &text, Point org, int fontFace, double fontScale, Scalar color, int thickness=1, int lineType=LINE_8, bool bottomLeftOrigin=false)
    cv2.putText(frame, d, (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
    cv2.imshow('video', frame)

video_stream()
root.mainloop()
