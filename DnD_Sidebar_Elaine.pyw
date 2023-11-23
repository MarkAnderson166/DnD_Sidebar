# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from random import *
from time import time, sleep
from tkinter.font import Font


#  GUI 
WIDTH = 250
HEIGHT = 500

root = tk.Tk()
root.title("DnD Sidebar Wildfire")
root.attributes('-topmost',True)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg='#211')
canvas.pack()
text_box_array = []

  # Notes Frame
notes_frame = tk.Frame(canvas, width=WIDTH-12, height=HEIGHT-130)
canvas.create_window(8, 8, window=notes_frame, anchor="nw")
notes_box = tk.Text(notes_frame, bg='#211', foreground='pink',
                    insertbackground='white', font=("Arial", 14),
                    bd=0, relief='ridge')
notes_box.place(x=0, y=0)

button_1_label = 'More Fire'
red_list_combat = ['Heroic', 'Terrified', 'Bloodthirsty',
                  'Hesitant', 'Desperate',
                  'Ruthless', 'Aggressive', 'Shaken', 
                  'Victorious', 'Wounded']
red_list_social = ['Relaxed', 'Anxious', 'Bored',
                  'Frustrated', 'Playful', 'Optimistic',
                  'Indifferent', 'Grateful', 'Impatient',
                  'Distrustful', 'Enthusiastic', 'Curious']

def fire_loop():
  while True:
    wildfire()
    tksleep(randint(60,600))
    #notes_box.configure(bg='#000')

def wildfire():
  social = choice(red_list_combat)
  combat = choice(red_list_social)

  font = Font(family="Times", size=13)
  social_width = font.measure(social)
  combat_width = font.measure(combat)

  pad = ''
  while social_width + combat_width + font.measure(pad) < WIDTH-18:
    pad = (pad+' ')

  text_box('%s%s%s' % (social, pad, combat))
  #canvas.configure(bg='#000')   


def text_box(text):
  canvas.delete('text_box_entry')
  text_box_array.append(text)
  y_offset = HEIGHT-35

  if len(text_box_array) > 4:
    text_box_array.pop(0)
    y_offset = HEIGHT-35

  shade = 250
  for line in reversed(text_box_array):
    y_offset = y_offset-20
    shade -= 50
    rgb = "#%02x%02x%02x" % ((shade),(shade),(shade))
    canvas.create_text(10, y_offset, anchor="nw",font="Times 13",
                       text= line, fill=rgb, tags='text_box_entry')


def open_notes():
  text_file = open("notes_elaine.txt", "r")
  notes = text_file.read()
  notes_box.insert("end-1c", notes)
  text_file.close()

def save():
  text_file = open("notes_elaine.txt", "w")
  text_file.write(notes_box.get(1.0, "end-1c"))
  text_file.close()
  text_box('    Notes saved')

def save_and_quit():
  save()
  quit()


def tksleep(t):
  text_box('next mood swing in %s seconds' % (t))

  ms = int(t*1000)
  root = tk._get_default_root('sleep')
  var = tk.IntVar(root)
  root.after(ms, var.set, 1)
  root.wait_variable(var)


  # buttons
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='#444', foreground='#fff', relief='flat')
style.map('TButton', background=[('active', '#555')])

btnS_X = 115
btnS_Y = 30

# bottom buttons
btn=ttk.Button(root, text='Wildfire', style="TButton",
                      command=wildfire).place(
                      x = 8, y = HEIGHT - btnS_Y - 5,
                      width = btnS_X, height = btnS_Y)

btn=ttk.Button(root, text="Exit", style="TButton",
                      command=save_and_quit).place(
                      x = btnS_X+15, y = HEIGHT - btnS_Y - 5,
                      width = btnS_X, height = btnS_Y)


open_notes()
fire_loop()
root.mainloop()
