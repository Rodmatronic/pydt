import tkinter as tk
from tkinter import Menu
from tkinter import messagebox
from tkinter import scrolledtext
import subprocess
import os
import getpass
import socket
import pyglet

pyglet.font.add_file("./Terminus.ttf")
hostname = socket.gethostname()
prompt = f"{hostname}# "

def donothing():
    pass

text_colour = "#FFB000"

class TerminalEmulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pydt")
        self.minsize(720, 440)
        self.geometry("720x300")
        self.option_add('*tearOff', False)
        self.configure(background='blue')  # Make closing/refreshing look prettier
        
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

        # Create a Canvas with a transparent image
        self.canvas = tk.Canvas(self, bg='blue', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create the ScrolledText widget and place it on top of the Canvas
        self.output_area = scrolledtext.ScrolledText(self.canvas, wrap=tk.WORD, font=("Terminus", 12), selectbackground="#e8973e", inactiveselectbackground="#e17600", bg="black", fg=text_colour, insertbackground="#e8973e", highlightthickness=0, borderwidth=0)
        self.output_area.place(relwidth=1, relheight=1)

        # Create a Canvas for the info_area
        self.info_canvas = tk.Canvas(self, width=200, height=20, bg='blue', highlightthickness=0)  # Set canvas height to 20
        self.info_canvas.pack(fill=tk.X)  # Fill only horizontally
        self.info_area = scrolledtext.ScrolledText(self.info_canvas, height=1, wrap=tk.WORD, font=("Terminus", 12), selectbackground="#e8973e", inactiveselectbackground="#e17600", bg="black", fg=text_colour, insertbackground="#e8973e", highlightthickness=0, borderwidth=0)
        self.info_area.pack(fill=tk.BOTH)  # Allow the info_area to fill the canvas

        self.output_area.bind("<Return>", self.execute_command)
        self.output_area.bind("<BackSpace>", self.disable_backspace)
        
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.cwd = os.getcwd()
        
        with open('/etc/motd', 'r') as f:
            self.output_area.insert(tk.END, f.read())

        # Define the tag with yellow background and black foreground
        self.info_area.tag_configure("highlight", background=text_colour, foreground="black")

        # Insert the text and apply the tag to "INPUT"
        self.info_area.insert(tk.END, "MODE: ")
        self.info_area.insert(tk.END, "INPUT", "highlight")
        self.info_area.config(state=tk.DISABLED)

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
