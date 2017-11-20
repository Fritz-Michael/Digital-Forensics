from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from tkinter import messagebox
from filerecoveryfunctions import *

class FileRecovery(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		
		self.controller = controller
		self.parent = parent

		self.start_sector_value = tk.IntVar()
		self.end_sector_value = tk.IntVar()
		self.thread_number_value = tk.IntVar()
		self.start_sector_value.set(1)
		self.end_sector_value.set(300000)
		self.thread_number_value.set(10)

		self.choose_drive_label = tk.Label(self.parent,text='Choose a Drive')
		self.choose_drive_list = tk.Listbox(self.parent,selectmode=tk.SINGLE,height=3,exportselection=False)
		self.choose_drive_scroll = tk.Scrollbar(self.parent,width=12)
		self.choose_drive_list.config(yscrollcommand=self.choose_drive_scroll.set)
		self.choose_drive_scroll.config(command=self.choose_drive_list.yview)
		self.choose_filetype_label = tk.Label(self.parent,text='Choose File Types')
		self.choose_filetype_list = tk.Listbox(self.parent,selectmode=tk.MULTIPLE,height=3,exportselection=False)
		self.choose_filetype_scroll = tk.Scrollbar(self.parent,width=12)
		self.choose_filetype_list.config(yscrollcommand=self.choose_filetype_scroll.set)
		self.choose_filetype_scroll.config(command=self.choose_filetype_list.yview)
		self.start_scan_button = tk.Button(self.parent,text='Start Scan',command=self.start_scan)
		self.advanced_button = tk.Button(self.parent,text='Advanced',command=self.advanced_settings)
		self.message_box = tk.Text(self.parent,state=tk.DISABLED,height=15,width=35)
		self.recover_files_button = tk.Button(self.parent,text='Recover Files',command=self.recover_files)

		self.set_drives()
		self.set_filetypes()

		self.choose_drive_label.grid(row=0,column=0)
		self.choose_drive_list.grid(row=1,column=0,rowspan=2)
		self.choose_drive_scroll.grid(row=1,column=1,rowspan=2,sticky=tk.W)

		self.choose_filetype_label.grid(row=0,column=2)
		self.choose_filetype_list.grid(row=1,column=2,rowspan=2)
		self.choose_filetype_scroll.grid(row=1,column=3,rowspan=2,sticky=tk.W)
		self.advanced_button.grid(row=3,column=2)
		self.message_box.grid(row=5,column=0,rowspan=2,columnspan=3,sticky=tk.W)
		self.start_scan_button.grid(row=7,column=0)
		self.recover_files_button.grid(row=7,column=2)

	def set_drives(self):
		self.drives = get_drivesWin()
		for key,drive in enumerate(self.drives):
			self.choose_drive_list.insert(key,drive)

	def set_filetypes(self):
		self.filetypes = getExtensions()
		for key,filetype in enumerate(self.filetypes):
			self.choose_filetype_list.insert(key,filetype)

	def advanced_settings(self):
		self.advanced_button.grid_remove()

		self.start_sector_label = tk.Label(self.parent,text='Start Sector: ')
		self.end_sector_label = tk.Label(self.parent,text='End Sector: ')
		self.thread_number_label = tk.Label(self.parent,text='Thread Number: ')
		self.start_sector_entry = tk.Entry(self.parent,textvariable=self.start_sector_value)
		self.end_sector_entry = tk.Entry(self.parent,textvariable=self.end_sector_value)
		self.thread_number_entry = tk.Entry(self.parent,textvariable=self.thread_number_value)

		self.start_sector_label.grid(row=3,column=0,sticky=tk.W)
		self.end_sector_label.grid(row=4,column=0,sticky=tk.W)
		self.start_sector_entry.grid(row=3,column=1,columnspan=2,sticky=tk.W)
		self.end_sector_entry.grid(row=4,column=1,columnspan=2,sticky=tk.W)
		self.thread_number_label.grid(row=3,column=3,sticky=tk.W)
		self.thread_number_entry.grid(row=3,column=4,columnspan=2,sticky=tk.W)

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