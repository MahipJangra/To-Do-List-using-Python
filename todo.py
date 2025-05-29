# To-Do List App with Light/Dark Theme, File Saving, and Scrollbar
from tkinter import *
from tkinter import messagebox
import os

# File to store tasks
FILENAME = "tasks.txt"

# Define Light and Dark Themes
light_theme = {
    "bg": "white",
    "fg": "black",
    "entry_bg": "white",
    "entry_fg": "black",
    "button_bg": "lightgray",
    "listbox_bg": "white",
    "listbox_fg": "black"
}

dark_theme = {
    "bg": "#2e2e2e",
    "fg": "white",
    "entry_bg": "#3e3e3e",
    "entry_fg": "white",
    "button_bg": "#505050",
    "listbox_bg": "#3e3e3e",
    "listbox_fg": "white"
}

# Start with light theme
current_theme = light_theme

# Load tasks from file into the listbox
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            for line in f:
                task_listbox.insert(END, line.strip())

# Save all current tasks from listbox to file
def save_tasks():
    with open(FILENAME, "w") as f:
        tasks = task_listbox.get(0, END)
        for task in tasks:
            f.write(task + "\n")

# Add a new task from the entry field
def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert(END, task)
        task_entry.delete(0, END)
        save_tasks()

# Remove the selected task from the listbox
def remove_task():
    try:
        selected = task_listbox.curselection()[0]
        task_listbox.delete(selected)
        save_tasks()
    except IndexError:
        pass  # Do nothing if no item is selected

# Prompt user for confirmation before exiting
def exit_app():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

# Switch between light and dark theme
def toggle_theme():
    global current_theme
    current_theme = dark_theme if current_theme == light_theme else light_theme
    apply_theme()

# Apply the current theme to all widgets
def apply_theme():
    root.configure(bg=current_theme["bg"])
    task_entry.configure(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["fg"])
    task_listbox.configure(bg=current_theme["listbox_bg"], fg=current_theme["listbox_fg"])
    
    for button in [add_button, remove_button, exit_button, theme_button]:
        button.configure(bg=current_theme["button_bg"], fg=current_theme["fg"], activebackground=current_theme["entry_bg"])

# ------------------- GUI Setup -------------------
root = Tk()
root.title("To-Do List")

# Task Entry field
task_entry = Entry(root, width=40)
task_entry.pack(pady=10)
task_entry.focus()  # Focus on entry when app starts

# Bind Enter key to add task
task_entry.bind("<Return>", lambda event: add_task())

# Add Task button
add_button = Button(root, text="Add Task", width=20, command=add_task)
add_button.pack()

# Remove Selected Task button
remove_button = Button(root, text="Remove Selected Task", width=20, command=remove_task)
remove_button.pack()

# Scrollbar and Listbox for task display
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

task_listbox = Listbox(root, width=50, height=10, yscrollcommand=scrollbar.set)
task_listbox.pack(pady=10)
scrollbar.config(command=task_listbox.yview)

# Exit and Theme Toggle buttons
exit_button = Button(root, text="Exit", width=20, command=exit_app)
exit_button.pack()

theme_button = Button(root, text="Toggle Dark Mode", width=20, command=toggle_theme)
theme_button.pack(pady=5)

# Load saved tasks and apply theme
load_tasks()
apply_theme()

# Start the application loop
root.mainloop()
