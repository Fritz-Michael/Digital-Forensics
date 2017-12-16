import tkinter as tk
from functools import partial
from filerecovery import *
from cleandrive import *
from encryption import *
from steganography import *
from aboutus import *

class main(tk.Tk):

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		self.title('Bulalords Forensic Tools')

		self.label = tk.Label(self,text='Welcome!')

		self.file_recovery_button = tk.Button(self,text='File Recovery',command=self.file_recovery,borderwidth=0)
		self.clean_drive_button = tk.Button(self,text='Clean Drive',command=self.clean_drive,borderwidth=0)
		self.encryption_button = tk.Button(self,text='Encryption',command=self.encryption,borderwidth=0)
		self.steganography_button = tk.Button(self,text='Steganography',command=self.steganography,borderwidth=0)
		self.about_us_button = tk.Button(self,text='About Us',command=self.about_us,borderwidth=0)

		self.frame_width = 500
		self.frame_height = 500
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)

		self.file_recovery_button.bind('<Enter>',partial(self.color_config,self.file_recovery_button,'green'))
		self.clean_drive_button.bind('<Enter>',partial(self.color_config,self.clean_drive_button,'green'))
		self.encryption_button.bind('<Enter>',partial(self.color_config,self.encryption_button,'green'))
		self.steganography_button.bind('<Enter>',partial(self.color_config,self.steganography_button,'green'))
		self.about_us_button.bind('<Enter>',partial(self.color_config,self.about_us_button,'green'))
		self.file_recovery_button.bind('<Leave>',partial(self.color_config,self.file_recovery_button,'black'))
		self.clean_drive_button.bind('<Leave>',partial(self.color_config,self.clean_drive_button,'black'))
		self.encryption_button.bind('<Leave>',partial(self.color_config,self.encryption_button,'black'))
		self.steganography_button.bind('<Leave>',partial(self.color_config,self.steganography_button,'black'))
		self.about_us_button.bind('<Leave>',partial(self.color_config,self.about_us_button,'black'))

		self.label.grid(row=0,column=3,columnspan=2)
		self.file_recovery_button.grid(row=1,columnspan=2,sticky=tk.W+tk.E)
		self.clean_drive_button.grid(row=2,columnspan=2,sticky=tk.W+tk.E)
		self.encryption_button.grid(row=3,columnspan=2,sticky=tk.W+tk.E)
		self.steganography_button.grid(row=4,columnspan=2,sticky=tk.W+tk.E)
		self.about_us_button.grid(row=5,columnspan=2,sticky=tk.W+tk.E)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)

	def color_config(self, widget, color, event):
		widget.configure(foreground=color)

	def file_recovery(self):
		self.label.config(text='File Recovery')
		self.function_frame.destroy()
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)
		self.function_frame.pack_propagate(False)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)
		FileRecovery(parent=self.function_frame,controller=self)

	def clean_drive(self):
		self.label.config(text='Clean Drive')
		self.function_frame.destroy()
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)
		self.function_frame.pack_propagate(False)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)
		CleanDrive(parent=self.function_frame,controller=self)

	def encryption(self):
		self.label.config(text='Encryption')
		self.function_frame.destroy()
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)
		self.function_frame.pack_propagate(False)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)
		Encryption(parent=self.function_frame,controller=self)


	def steganography(self):
		self.label.config(text='Steganography')
		self.function_frame.destroy()
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)
		self.function_frame.pack_propagate(False)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)
		Steganography(parent=self.function_frame,controller=self)


	def about_us(self):
		self.function_frame.destroy()
		self.function_frame = tk.Frame(self,width=self.frame_width,height=self.frame_height,bg=None,highlightthickness=2,highlightbackground='black')
		self.function_frame.grid_propagate(False)
		self.function_frame.pack_propagate(False)
		self.function_frame.grid(row=1,column=2,rowspan=5,columnspan=5)
		AboutUs(parent=self.function_frame,controller=self)

	def exit(self):
		self.quit()

if __name__ == '__main__':
	GUI = main()
	GUI.mainloop()