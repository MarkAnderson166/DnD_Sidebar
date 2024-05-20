# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
import sys
from tkinter import ttk
from random import *
from time import time, sleep
from tkinter.font import Font

#  GUI 
WIDTH = 320
HEIGHT = 900
global page
page = "songs"

root = tk.Tk()
root.title("DnD Sidebar")
root.attributes('-topmost',True)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg='#211')
canvas.pack()
text_box_array = []

  # Notes Frame
notes_frame = tk.Frame(canvas, width=WIDTH-12, height=HEIGHT-12)
canvas.create_window(8, 8, window=notes_frame, anchor="nw")
notes_box = tk.Text(notes_frame, bg='#211', foreground='pink',
                    insertbackground='white', font=("Arial", 14),
                    bd=0, relief='ridge')
notes_box.place(x=0, y=0, width=WIDTH-12, height=HEIGHT-110)

def songs():
  global page
  page = "songs"
  open_notes()
def inventory():
  global page
  page = "inventory"
  open_notes()
def notes():
  global page
  page = "notes"
  open_notes()

def open_notes():
  text_file = open("stone_%s.txt"%page, "r")
  notes = text_file.read()
  notes_box.delete('1.0', tk.END)
  notes_box.insert("end-1c", notes)
  text_file.close()

def save():
  text_file = open("stone_%s.txt"%page, "w")
  text_file.write(notes_box.get(1.0, "end-1c"))
  text_file.close()

  # buttons
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='#444', foreground='#fff', relief='flat')
style.map('TButton', background=[('active', '#555')])

btnS_X1 = 98
btnS_X2 = 149
btnS_Y = 30

# bottom buttons
btn=ttk.Button(root, text='Songs', style="TButton",
                      command=songs).place(
                      x = 10, y = HEIGHT - btnS_Y*3 - 10,
                      width = btnS_X1, height = btnS_Y*2)

btn=ttk.Button(root, text='Inventory', style="TButton",
                      command=inventory).place(
                      x = btnS_X1+15, y = HEIGHT - btnS_Y*3 - 10,
                      width = btnS_X1, height = btnS_Y*2)

btn=ttk.Button(root, text='Notes', style="TButton",
                      command=notes).place(
                      x = btnS_X1*2+20, y = HEIGHT - btnS_Y*3 - 10,
                      width = btnS_X1, height = btnS_Y*2)

btn=ttk.Button(root, text="Save", style="TButton",
                      command=save).place(
                      x = 10, y = HEIGHT - btnS_Y - 6,
                      width = btnS_X2, height = btnS_Y)

btn=ttk.Button(root, text="Exit", style="TButton",
                      command=sys.exit).place(
                      x = btnS_X2+15, y = HEIGHT - btnS_Y - 6,
                      width = btnS_X2, height = btnS_Y)

open_notes()
root.mainloop()
