from PIL import ImageTk, Image
from functools import partial
import tkinter as tk

class AboutUs(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent
		self.label = tk.Label(self.parent,text='This is for About Us')
		self.label.grid(row=0)