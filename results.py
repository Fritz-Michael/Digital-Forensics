import tkinter as tk

class ResultWindow(tk.Tk):

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		self.title('Results')

		self.text = tk.StringVar(self)
		self.key = tk.IntVar(self)

		self.label_message = tk.Label(self,text='Message:')
		self.result = tk.Text(self,height=5,width=30)
		self.label_key = tk.Label(self,text='Key:')
		self.entry = tk.Text(self,height=1,width=30)

		self.resizable(False,False)
		self.label_message.pack()
		self.result.pack()
		self.label_key.pack()
		self.entry.pack()


	def set_results(self,message,key):
		self.result.insert(tk.END,message)
		self.entry.insert(tk.END,key)
		
		self.result.config(state=tk.DISABLED)
		self.entry.config(state=tk.DISABLED)
