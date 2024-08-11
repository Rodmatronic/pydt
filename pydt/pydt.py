import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import os
import getpass
import socket
import pyglet
import time

pyglet.font.add_file("./Terminus.ttf")
hostname = socket.gethostname()
prompt = f"{hostname}# "

def donothing():
    pass

class TerminalEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pydt")
        self.geometry("720x401")
        self.option_add('*tearOff', False)
        self.configure(background='black') # Make closing/refreshing look prettier
        
        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Preferences", command=self.preferences)
        self.filemenu.add_separator() 
        self.filemenu.add_command(label="Exit", command=self.quit_with_style)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=donothing)
        self.helpmenu.add_command(label="About...", command=self.info_msg)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.config(menu=self.menubar)

        self.output_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Terminus", 12), bg="black", fg="#e8973e", insertbackground="#e8973e", highlightthickness = 0, borderwidth=0)
        self.output_area.pack(fill=tk.BOTH, expand=True)
        self.output_area.bind("<Return>", self.execute_command)
        self.output_area.bind("<BackSpace>", self.disable_backspace)
        
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.cwd = os.getcwd()
        
        with open('/etc/motd', 'r') as f:
            self.output_area.insert(tk.END, f.read())

        #self.prompt = f"|-[({self.username}@{self.hostname})-({self.cwd})]\n|-$ "
        self.prompt = prompt
        self.output_area.insert(tk.END, self.prompt)
        self.output_area.mark_set("prompt_end", "insert")
        self.output_area.mark_gravity("prompt_end", tk.LEFT)
        self.output_area.focus()

    def quit_with_style(self):
        response = messagebox.askyesno("Confirmation", "Are you sure you want to exit the terminal?")
        if response:  # User clicked "Yes"
          print("User clicked Yes, exiting")
          exit()
        else:  # User clicked "No"
          print("User clicked No.")

    def info_msg(self): 
        messagebox.showinfo("About", "Python Dumb Terminal (pydt), a really, really dumb terminal. Written by Rodmatronics") 
    
    def preferences(self): 
        x = 1

        #pref_window = tk.Toplevel(self)
        #pref_window.title("Preferences")

        #tk.Label(pref_window, text="Foreground Color:").grid(row=0, column=0, padx=5, pady=5)
        #self.fg_color_entry = tk.Entry(pref_window)
        #self.fg_color_entry.insert(0, self.fg_color)
        #self.fg_color_entry.grid(row=0, column=1, padx=5, pady=5)

        #tk.Label(pref_window, text="Background Color:").grid(row=1, column=0, padx=5, pady=5)
        #self.bg_color_entry = tk.Entry(pref_window)
        #self.bg_color_entry.insert(0, self.bg_color)
        #self.bg_color_entry.grid(row=1, column=1, padx=5, pady=5)

        #tk.Label(pref_window, text="Show /etc/motd:").grid(row=2, column=0, padx=5, pady=5)
        #self.motd_var = tk.BooleanVar(value=self.show_motd)
        #tk.Checkbutton(pref_window, variable=self.motd_var).grid(row=2, column=1, padx=5, pady=5)

        #tk.Button(pref_window, text="Save", command=self.save_preferences).grid(row=3, column=0, columnspan=2, pady=10)

        #self.output_area.configure(bg="White")

    def execute_command(self, event):
        command = self.get_current_command().strip()
        self.output_area.insert(tk.END, "\n")
        
        if command:
            if command.startswith("cd "):
                try:
                    os.chdir(command.split(" ", 1)[1])
                except FileNotFoundError as e:
                    self.output_area.insert(tk.END, f"cd: {str(e)}\n")
                self.cwd = os.getcwd()
            elif command.startswith("exit"):
                exit()
            elif command.startswith("clear"):
                self.output_area.delete(1.0, tk.END)
                self.output_area.insert(tk.END, "")
            else:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                    self.output_area.insert(tk.END, output)
                except subprocess.CalledProcessError as e:
                    self.output_area.insert(tk.END, e.output)
        self.update_prompt()
        return "break"

    def disable_backspace(self, event):
        if self.output_area.compare("insert", ">", "prompt_end"):
            return None
        else:
            return "break"

    def update_prompt(self):
        self.prompt = prompt
        self.output_area.insert(tk.END, self.prompt)
        self.output_area.mark_set("prompt_end", "insert")
        self.output_area.see(tk.END)

    def get_current_command(self):
        last_line = self.output_area.get("prompt_end", "insert lineend")
        return last_line

if __name__ == "__main__":
    app = TerminalEmulator()
    app.mainloop()

