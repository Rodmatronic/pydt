from tkinter import *
import subprocess
import socket
import os

# Create a GUI window
root = Tk()

root.title("Pydt")
root.minsize(484, 364)
root.geometry("484x364")
root.configure(background='#170e05') 
user_text = []
cursor_x, cursor_y = 0, 0
line_height = 20  # Height between lines
current_command = ""  # Buffer to store the current command

darkest_dark = "#261800"
middle_dark = "#56340d"
lightest_dark = "#8c5700"

# Get the current hostname
hostname = socket.gethostname()
prompt = f"{hostname}$ "  # Set the prompt with the hostname

def stroke_text(x, y, text, textcolor, strokecolor):
    # second layer
    canvas.create_text(x + 8 - 3, y + 13, text=text, font=('Terminus', 12, 'bold'), fill=strokecolor)
    canvas.create_text(x + 8 +2, y + 13, text=text, font=('Terminus', 12, 'bold'), fill=strokecolor)
    canvas.create_text(x + 8, y + 15, text=text, font=('Terminus', 12, 'bold'), fill=strokecolor)
    canvas.create_text(x + 8, y + 11, text=text, font=('Terminus', 12, 'bold'), fill=strokecolor)

    # first layer
    canvas.create_text(x + 8 - 1, y + 13, text=text, font=('Terminus', 12, 'bold'), fill="#8c5700")
    canvas.create_text(x + 8 , y + 13, text=text, font=('Terminus', 12, 'bold'), fill="#8c5700")
    canvas.create_text(x + 8, y + 14, text=text, font=('Terminus', 12, 'bold'), fill="#8c5700")

    # make regular text
    canvas.create_text(x + 8, y + 13, text=text, font=('Terminus', 12), fill=textcolor)

def print_term(x, y, text, textcolor, strokecolor):
    for i, char in enumerate(text):
        char_x = x + i * 11  # Calculate the x position for each character
        stroke_text(char_x, y, char, textcolor, strokecolor)

def render_text():
    canvas.delete("all")  # Clear the canvas to redraw the text
    global cursor_x, cursor_y

    cursor_x, cursor_y = 0, 0  # Reset cursor position

    for line in user_text:
        print_term(0, cursor_y, line, '#FFB000', '#56340d')
        cursor_y += line_height  # Move cursor to next line

    draw_cursor()

def draw_cursor():
    # Draw the block text cursor at the end of the last line
    if user_text:
        cursor_x = len(user_text[-1]) * 11  # Calculate x position based on text length
        canvas.create_rectangle(cursor_x + 2, cursor_y - line_height + 2, cursor_x + 16, cursor_y + 2, outline=darkest_dark, fill=middle_dark)
        canvas.create_rectangle(cursor_x + 4, cursor_y - line_height + 4, cursor_x + 14, cursor_y + 0, outline=lightest_dark, fill='#FFB000')

def execute_command(command):
    global current_command
    
    if command.startswith("cd "):
        try:
            # Change the current working directory
            os.chdir(command[3:].strip())
        except FileNotFoundError as e:
            user_text.append(f"cd: No such file or directory: {command[3:].strip()}")
        except NotADirectoryError as e:
            user_text.append(f"cd: Not a directory: {command[3:].strip()}")
        except PermissionError as e:
            user_text.append(f"cd: Permission denied: {command[3:].strip()}")
    elif command == "clear":
        user_text.clear()  # Clear the terminal display
    else:
        try:
            # Execute other commands and capture the output
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            output = e.output  # In case of error, capture the output
        user_text.append(output)  # Append the output to the terminal display

def on_key_press(event):
    global user_text, current_command
    if event.keysym == "BackSpace":
        if user_text and len(user_text[-1]) > len(prompt):  # Allow backspace only if not at the prompt
            user_text[-1] = user_text[-1][:-1]  # Remove the last character
            current_command = current_command[:-1]  # Remove last character from command buffer
    elif event.keysym == "Return":
        if current_command.strip():  # Only execute if command is not empty
            execute_command(current_command)  # Execute the current command
        current_command = ""  # Clear the command buffer
        user_text.append(prompt)  # Add a new prompt line
    else:
        user_text[-1] += event.char  # Add the typed character to the last line
        current_command += event.char  # Add the character to the command buffer

    render_text()

canvas = Canvas(root, bg='#170e05', width=500, height=500, highlightthickness=0)
canvas.pack(fill=BOTH)

# Start with the prompt
user_text.append(prompt)
render_text()

# Bind key press events to the function
root.bind("<KeyPress>", on_key_press)

mainloop()