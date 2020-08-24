import functools
from tkinter import *

root = Tk()
def func(name):
    print (name)
mylist = ['item1','item2','item3']
for item in mylist:
    button = Button(root,text=item,command=functools.partial(func,item))
    button.pack()

root.mainloop()