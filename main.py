import serial
import threading
import json
from tkinter import *


with open('conf.json', 'r') as f:
    conf = json.loads("".join(f.read()))


BACKGROUND      = conf['background']
FOREGROUND      = conf['foreground'] 
PORT            = conf['port']


ser             = serial.Serial()
ser.baudrate    = int(conf['baud'])
ser.port        = PORT
not_closed      = True 
ser.open()

window = Tk()

def close_window():
    ser.close() 
    window.destroy()

window.title('Serial Port reader')
window.resizable(0,0)
window.configure(background=BACKGROUND)
window.minsize(600,400)

Label(window, text=f"Serial Port {PORT}", bg=BACKGROUND, fg=FOREGROUND).grid(row=1, column=0, sticky=W)

term = Text(bd=0, bg=BACKGROUND, fg=FOREGROUND)
term.grid(row=3, column=0, sticky=W)
term.bind("<Key>", lambda e: "break")
term.see(END)

def get_last():
    while not_closed:
        if read := ser.read():
            term.insert(END, read)
            term.see(END)

def start_button():
    t1 = threading.Thread(target=get_last, daemon=True, args=())
    t1.start()

buttons = Frame(window)
start = Button(buttons,  text="Start", width=42, command=start_button, fg=FOREGROUND, bg=BACKGROUND)
close = Button(buttons,  text="Close", width=42, command=close_window, bg=BACKGROUND, fg=FOREGROUND)

buttons.grid(row=4, column=0, sticky='nsew')

start.pack(side="left")
close.pack(side="right")

window.mainloop()
