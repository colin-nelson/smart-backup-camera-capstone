from guizero import App, PushButton, TextBox, Text, Slider


def change_offset(slider_value):
    Offset.value = slider_value
    
def increase_offset():
    Offset.value = int(Offset.value) + 1
    

def decrease_offset():
    Offset.value = int(Offset.value) - 1
#def change_display():
#    Offeset.

def return_offset():
    return int(Offset.value)
    
def close_window():
    app.destroy()
    
#Name of the app
app = App(title ="GUI")
text = Text(app, text ="Current Offset", size = 40)
Offset = Text(app, text="0", size = 30)

pButton = PushButton(app, text = "+", command = increase_offset, align="right")
mButton = PushButton(app, text = "-", command = decrease_offset, align="left")
#bSlider = Slider(


exit = PushButton(app, text = "confirm", command = close_window)
#offval = int(offset.value)




app.display()
