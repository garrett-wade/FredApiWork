import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import os
from seriesData import dict_IDs
import pprint
from fredapi import Fred

fred = Fred(api_key='129c1c0d602287cb65291a2166295ce1')

class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Fed Challange Data Management")

        container = tk.Frame(self)
        container.configure()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_frame2(self, cont, ID, col_header, operator):

        try:
            fred.get_series(series_id=ID)

        except:
            messagebox.showerror('Error','ID Invalid')
            stop

        if ID in dict_IDs.keys():
            messagebox.showerror('Error','ID Already in use')
            stop
        else:
            dict_IDs[ID] = [col_header, operator]
            frame = self.frames[cont]
            file = open('seriesData.py', 'w')
            file.write('dict_IDs = ' + pprint.pformat(dict_IDs))
            file.close()
            frame.tkraise()

    def close_window(self):
        self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        calculations = ['PCT_CHANGE']
        var1 = StringVar()

        label1 = ttk.Label(self,text='Copy series ID from FRED into box below:')
        entry1 = ttk.Entry(self,width=40)
        label2 = ttk.Label(self,text='Type dersired column header in the box below: ')
        entry2 = ttk.Entry(self,width=40)
        label3 = ttk.Label(self,text='Select desired calcuation from the picklist below: ')
        picklist1 = ttk.OptionMenu(self,var1,'Select Operator', *calculations)
        button1 = ttk.Button(self,text='Add Series',
                             command=lambda:controller.show_frame2(PageOne,
                                                                  entry1.get(),
                                                                  entry2.get(),
                                                                  var1.get()))

        label1.pack(padx=(20,20),pady=(20,10))
        entry1.pack(padx=(20,20),pady=(0,10))
        label2.pack(padx=(20,20),pady=(0,10))
        entry2.pack(padx=(20,20),pady=(0,10))
        label3.pack(padx=(20,20),pady=(0,10))
        picklist1.pack(padx=(20,20),pady=(0,10))
        picklist1.configure(width=35)
        button1.pack(padx=(20,20),pady=(0,20))


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label1 = ttk.Label(self,text='Series succesfully added')
        button1 = ttk.Button(self,text='Add Another',command=lambda:controller.show_frame(StartPage))
        button2 = ttk.Button(self,text='Close',command=lambda:controller.close_window())

        label1.pack(padx=(20,20),pady=(60,10))
        button1.pack(padx=(20,20),pady=(10,10))
        button2.pack(padx=(20,20),pady=(10,20))

def main():
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
