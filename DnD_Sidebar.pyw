# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from random import *

# button functions

button_1_label = '1'
red_list = ['1','2']
def button_1_func():
  text_box('Red: %s' % choice(red_list) )

button_2_label = '2'
def button_2_func():
  dice(2,6,5)

button_3_label = '3'
def button_3_func():
  dice(3,8,6)

button_4_label = '4'
def button_4_func():
  dice(4,12,7)



def text_box(text):
  canvas.delete('text_box_entry')
  text_box_array.append(text)
  y_offset = HEIGHT-50

  if len(text_box_array) > 7:
      text_box_array.pop(0)
      y_offset = HEIGHT-50

  shade = 250
  for line in reversed(text_box_array):
      y_offset = y_offset-20
      shade -= 25
      rgb = "#%02x%02x%02x" % ((shade),(shade),(shade))

      canvas.create_text(10, y_offset, anchor="nw",font="Times 13",
                         text= line, fill=rgb, tags='text_box_entry')


def dice(number,dice,plus):
  result = plus
  for i in range(number):
    roll = randint(1,dice)
    result = result+roll
  text_box('%sd%s+%s = %s'%(number, dice, plus, result))
  return result


def open_notes():
  text_file = open("notes.txt", "r")
  notes = text_file.read()
  notes_box.insert("end-1c", notes)
  text_file.close()

  text_file = open("names.txt", "r")
  names = text_file.read()

      #remove last sessions initiative rolls
  for name in names:
    name = name.translate(translation_table)
    names_box.insert("end-1c", name)
  text_file.close()

def save():
  text_file = open("notes.txt", "w")
  text_file.write(notes_box.get(1.0, "end-1c"))
  text_file.close()
  text_box('Notes saved')

  text_file = open("names.txt", "w")
  text_file.write(names_box.get(1.0, "end-1c"))
  text_file.close()
  text_box('Names saved')

def save_and_quit():
  save()
  quit()


def move_turn_arrow():

  pointer = ''
  int_rolls = int_roll_box.get(1.0, "end-1c")
  pad = len(int_rolls.split('\n'))
  players = len(names_box.get(1.0, "end-1c").split('\n'))

  if any(char.isdigit() for char in int_rolls) and not pad == players:
    text_box('wrong button?, you must set before next')

  else:

    for i in range(pad):
      pointer = '\n%s' % pointer  
    pointer = pointer+ '>'
    if pad == players-1: pointer = '>'

    int_roll_box.delete("1.0","end-1c")
    int_roll_box.insert("end-1c", pointer)


def sort_initiative():

  int_roll = int_roll_box.get(1.0, "end-1c").split('\n')
  players = names_box.get(1.0, "end-1c").split('\n')

  while('' in int_roll):int_roll.remove('')
  while('' in players):players.remove('')

  if len(int_roll) != len(players):
    text_box('1 roll per character is required, you have')
    text_box('entered %s rolls for %s characters'% (len(int_roll),len(players)))

  else:
    int_roll_box.delete("1.0","end-1c")
    int_roll_box.insert("end-1c", '>')

    names_box.delete("1.0","end-1c")
    players_sorted = []
    for i in range(len(players)):
      name = players[i].translate(translation_table)
      roll = int_roll[i]
      if len(roll) == 1:
        roll = '0%s'%roll
      name = '%s - %s\n' % (roll, name)
      players_sorted.append(name)

    players_sorted = sorted(players_sorted, key=lambda s: int(s[:2]),reverse=1)
    for name in players_sorted:
      names_box.insert("end-1c", name)


#  GUI 

WIDTH = 320
HEIGHT = 650

root = tk.Tk()
root.title("DnD Sidebar")
root.attributes('-topmost',True)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg='#111')
canvas.pack()
text_box_array = []
translation_table = str.maketrans('', '', '0123456789 -')


notes_frame = tk.Frame(canvas, width=WIDTH-165, height=HEIGHT/2-5, bg='#111')
canvas.create_window(5, 5, window=notes_frame, anchor="nw")
notes_box = tk.Text(notes_frame, bg='#112', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
notes_box.place(x=5, y=5)

turn_frame = tk.Frame(canvas, width=30, height=HEIGHT/2-5, bg='#111')
canvas.create_window(WIDTH-160, 5, window=turn_frame, anchor="nw")
int_roll_box = tk.Text(turn_frame, bg='#121', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
int_roll_box.place(x=5, y=5)

turn_frame = tk.Frame(canvas, width=125, height=HEIGHT/2-5, bg='#111')
canvas.create_window(WIDTH-130, 5, window=turn_frame, anchor="nw")
names_box = tk.Text(turn_frame, bg='#211', foreground="light grey",
                  insertbackground='white', font=("Arial", 14),
                  bd=0, relief='ridge')
names_box.place(x=5, y=5)


  # buttons

style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='#444', foreground='#fff', relief='flat')
style.map('TButton', background=[('active', '#555')])

btnO_Y = 320
btnS_X = 100
btnS_Y = 60


# main 4 buttons
buttonReset=ttk.Button(root, text=button_1_label, style="TButton",
                      command=button_1_func).place(
                      x=5, y=HEIGHT-btnO_Y,
                      width=btnS_X, height=btnS_Y)

buttonReset=ttk.Button(root, text=button_2_label, style="TButton",
                      command=button_2_func).place(
                      x=11+btnS_X, y=HEIGHT-btnO_Y,
                      width=btnS_X, height=btnS_Y)

buttonReset=ttk.Button(root, text=button_3_label, style="TButton",
                      command=button_3_func).place(
                      x=5, y=HEIGHT-btnO_Y+btnS_Y+5,
                      width=btnS_X, height=btnS_Y)

buttonReset=ttk.Button(root, text=button_4_label, style="TButton",
                      command=button_4_func).place(
                      x=11+btnS_X, y=HEIGHT-btnO_Y+btnS_Y+5,
                      width=btnS_X, height=btnS_Y)


# turn tracker buttons
buttonReset=ttk.Button(root, text="Next", style="TButton",
                      command=move_turn_arrow).place(
                      x=17+btnS_X*2, y=HEIGHT-btnO_Y,
                      width=btnS_X, height=btnS_Y)

buttonReset=ttk.Button(root, text="Set Initiative", style="TButton",
                      command=sort_initiative).place(
                      x=17+btnS_X*2, y=HEIGHT-btnO_Y+btnS_Y+5,
                      width=btnS_X, height=btnS_Y)


# bottom buttons
buttonReset=ttk.Button(root, text="Save", style="TButton",
                      command=save).place(
                      x=5, y=HEIGHT-btnS_Y/1.5-5,
                      width=btnS_X, height=btnS_Y/1.5)

buttonReset=ttk.Button(root, text="About", style="TButton",
                      command=save).place(
                      x=11+btnS_X, y=HEIGHT-btnS_Y/1.5-5,
                      width=btnS_X, height=btnS_Y/1.5)

buttonReset=ttk.Button(root, text="Exit", style="TButton",
                      command=save_and_quit).place(
                      x=17+btnS_X*2, y=HEIGHT-btnS_Y/1.5-5,
                      width=btnS_X, height=btnS_Y/1.5)


  # -- mouse
def click(event):
  text_box('mouse click at %s , %s ' % (event.x, event.y))
canvas.bind('<Button-1>', click)

open_notes()
root.mainloop()
