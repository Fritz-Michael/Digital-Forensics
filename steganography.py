from functools import partial
import tkinter as tk
from tkinter import *
from tkinter import ttk

class Steganography(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent

		self.label = tk.Label(self.parent,text='sample')

		self.label.pack()

	def conceal_init(self):
		pass

	def reveal_init(self):
		pass