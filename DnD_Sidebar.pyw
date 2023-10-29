# ------------------------------------------------------------
# --------- Mark Anderson ------------------------------------
# ------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
from random import *

WIDTH = 300
HEIGHT = 800

root = tk.Tk()
root.title("DnD Sidebar")
root.attributes('-topmost',True)
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
canvas.configure(bg='#222')

text_box_array = []



def text_box(text):

  canvas.delete('text_box_entry')
  text_box_array.append(text)
  y_offset = HEIGHT

  if len(text_box_array) > 7:
      text_box_array.pop(0)
      y_offset = HEIGHT

  shade = 250
  for line in reversed(text_box_array):
      y_offset = y_offset-20
      shade -= 25
      rgb = "#%02x%02x%02x" % ((shade),(shade),(shade))

      canvas.create_text(5, y_offset, anchor="nw",font="Times 13",text= line, fill=rgb, tags='text_box_entry')



def dice(number,dice,plus,name):
  arr = []
  result = plus
  for i in range(number):
    roll = randint(1,dice)
    result = result+roll
    arr.append(roll)
  arr.append(plus)
  text_box('%s rolled %s (%sd%s+%s) = %s'%(name, arr, number, dice, plus, result))
  return result







    # buttons
style = ttk.Style()
style.theme_use("clam")
style.configure('TButton', background='#444', foreground='#fff', relief='flat')
style.map('TButton', background=[('active', '#555')])

buttonReset=ttk.Button(root, text="Start", width=20,command=lambda:dice(2,10,5,'Player'), style="TButton")
buttonReset.place(x=10, y=HEIGHT-500)
buttonSolve=ttk.Button(root, text="Stop", width=20, command=lambda:resetMap(), style="TButton")
buttonSolve.place(x=120, y=HEIGHT-400)
buttonDLC=ttk.Button(root, text="Spray", width=20, command=lambda:dice(4,8,randint(1,10),'Player'), style="TButton")
buttonDLC.place(x=10, y=HEIGHT-300)
buttonExit=ttk.Button(root, text="Exit", width=20, command=root.destroy, style="TButton")
buttonExit.place(x=120, y=HEIGHT-200)






  # -- mouse
def click(event):
  text_box('mouse click at %s , %s ' % (event.x, event.y))
canvas.bind('<Button-1>', click)

root.mainloop()
