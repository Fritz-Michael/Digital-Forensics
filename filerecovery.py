from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from filerecoveryfunctions import *

class FileRecovery(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		
		self.controller = controller
		self.parent = parent
		self.settings_frame = tk.Frame(self.parent,bd=2,relief=tk.SUNKEN)
		self.initialize_settings_frame()
		self.alignment_frames.append(tk.Frame(self.parent))

		self.start_scan_button = tk.Button(self.alignment_frames[1],text='Start Scan',command=self.start_scan)
		self.advanced_button = tk.Button(self.alignment_frames[1],text='Advanced',command=self.advanced_settings)
		self.recover_files_button = tk.Button(self.alignment_frames[1],text='Recover Files',command=self.recover_files)

		self.settings_frame.pack(fill=tk.X)
		self.alignment_frames[1].pack(side=tk.TOP)
		self.advanced_button.pack(side=tk.LEFT,padx=5,pady=10)
		self.start_scan_button.pack(side=tk.LEFT,padx=5,pady=10)
		self.recover_files_button.pack(side=tk.LEFT,padx=5,pady=10)

	def initialize_settings_frame(self):
		self.directory = '/'
		self.start_sector_value = tk.IntVar()
		self.end_sector_value = tk.IntVar()
		self.thread_number_value = tk.IntVar()

		self.start_sector_value.set(1)
		self.end_sector_value.set(300000)
		self.thread_number_value.set(10)

		self.alignment_frames = []
		self.alignment_frames.append(tk.Frame(self.settings_frame))
		self.choose_drive_label = tk.Label(self.settings_frame,text='Choose a Drive')
		self.choose_filetype_menu = tk.Menubutton(self.alignment_frames[0],text='Choose File Types',relief=tk.RAISED)
		self.choose_directory_button = tk.Button(self.alignment_frames[0],text='Select Directory',command=self.choose_directory)

		self.set_drives()
		self.set_filetypes()

		self.alignment_frames[0].pack(side=tk.TOP,pady=8)
		self.choose_drive_list.pack(side=tk.LEFT,pady=8)
		self.choose_filetype_menu.pack(side=tk.LEFT,pady=8)
		self.choose_directory_button.pack(side=tk.LEFT)

	def choose_directory(self):
		self.directory = filedialog.askdirectory(initialdir=self.directory,title='Select Directory')

	def set_drives(self):
		self.drives = get_drivesWin()
		self.default_drive = tk.StringVar(self.parent)
		self.default_drive.set(self.drives[0])
		self.choose_drive_list = tk.OptionMenu(self.alignment_frames[0],self.default_drive,*self.drives)

	def set_filetypes(self):
		self.choose_filetype_menu.menu = tk.Menu(self.choose_filetype_menu,tearoff=0)
		self.choose_filetype_menu['menu'] = self.choose_filetype_menu.menu
		self.filetypes = getExtensions()
		self.filetypes_index = []
		for key,filetype in enumerate(self.filetypes):
			self.filetypes_index.append(tk.IntVar())
			self.filetypes_index[key].set(key)
			self.choose_filetype_menu.menu.add_checkbutton(label=self.filetypes[key],variable=self.filetypes_index[key])


	def advanced_settings(self):
		self.advanced_button.pack_forget()
		self.alignment_frames.append(tk.Frame(self.settings_frame))
		self.alignment_frames.append(tk.Frame(self.settings_frame))
		self.alignment_frames.append(tk.Frame(self.settings_frame))
		self.start_sector_label = tk.Label(self.alignment_frames[2],text='Start Sector: ')
		self.end_sector_label = tk.Label(self.alignment_frames[3],text='End Sector: ')
		self.thread_number_label = tk.Label(self.alignment_frames[4],text='Thread Number: ')
		self.start_sector_entry = tk.Entry(self.alignment_frames[2],textvariable=self.start_sector_value)
		self.end_sector_entry = tk.Entry(self.alignment_frames[3],textvariable=self.end_sector_value)
		self.thread_number_entry = tk.Entry(self.alignment_frames[4],textvariable=self.thread_number_value)

		self.alignment_frames[2].pack(pady=3)
		self.alignment_frames[3].pack(pady=3)
		self.alignment_frames[4].pack(pady=3)
		self.start_sector_label.pack(side=tk.LEFT)
		self.start_sector_entry.pack(side=tk.LEFT)
		self.end_sector_label.pack(side=tk.LEFT)
		self.end_sector_entry.pack(side=tk.LEFT)
		self.thread_number_label.pack(side=tk.LEFT)
		self.thread_number_entry.pack(side=tk.LEFT)

	def start_scan(self):
		if self.choose_drive_list.curselection() == ():
			messagebox.showwarning('Error','Choose a Drive!')
		else:
			self.selected_drive = self.drives[self.choose_drive_list.curselection()[0]]
			self.path = '\\\\.\\' + self.selected_drive + ':'
			self.root_path = self.selected_drive

		if self.choose_filetype_list.curselection() == ():
			messagebox.showwarning('Error','Choose a File type to recover!')
		else:
			self.selected_drive = self.drives[self.choose_drive_list.curselection()[0]]

		try:
			self.start_sector_value = int(self.start_sector_entry.get())
			self.end_sector_value = int(self.end_sector_entry.get())
			self.thread_number_value = int(self.thread_number_entry.get())
		except ValueError:
			messagebox.showwarning('Error','Incorrect Input!')
		except AttributeError:
			self.start_sector_value = 1
			self.end_sector_value = gettotalsectors(self.path)
			self.thread_number_value = 10
		except BaseException as er:
			messagebox.showwarning('Error',er)

	def recover_files(self):
		pass