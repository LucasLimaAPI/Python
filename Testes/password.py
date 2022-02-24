import numbers
import random
from tkinter import messagebox

lower= "abcdefghijklmnopqrstuvwxyz"
upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers= "012346789"
symbols= "[] {} () * ; / _-"

all = lower + upper + numbers +symbols

length = 16
password = " ".join(random.sample(all,length))

messagebox.askyesno('Gerador de senha aleatória',\
                      password)











