import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from a file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to a file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Create the main application window
root = tk.Tk()
root.title("To-Do List App")

# Load existing tasks
tasks = load_tasks()

# Function to add a task to the list
def add_task():
    task = task_entry.get()
    if task != "":
        task_listbox.insert(tk.END, task)
        tasks.append(task)
        save_tasks(tasks)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# Function to remove the selected task from the list
def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
        tasks.pop(selected_task_index)
        save_tasks(tasks)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Function to mark a task as completed
def mark_completed():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task = task_listbox.get(selected_task_index)
        task_listbox.delete(selected_task_index)
        updated_task = task + " (Completed)"
        task_listbox.insert(tk.END, updated_task)
        tasks[selected_task_index] = updated_task
        save_tasks(tasks)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to mark as completed.")

# Function to clear all tasks
def clear_all():
    task_listbox.delete(0, tk.END)
    tasks.clear()
    save_tasks(tasks)

# Function to edit a task
def edit_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        current_task = task_listbox.get(selected_task_index)
        new_task = simpledialog.askstring("Edit Task", "Edit the task:", initialvalue=current_task)
        if new_task:
            task_listbox.delete(selected_task_index)
            task_listbox.insert(selected_task_index, new_task)
            tasks[selected_task_index] = new_task
            save_tasks(tasks)
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

# Create and configure the widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

task_entry = tk.Entry(frame, width=40)
task_entry.grid(row=0, column=0, padx=5)

add_task_button = tk.Button(frame, text="Add Task", width=20, command=add_task)
add_task_button.grid(row=0, column=1, padx=5)

delete_task_button = tk.Button(frame, text="Delete Task", width=20, command=delete_task)
delete_task_button.grid(row=1, column=0, padx=5)

mark_completed_button = tk.Button(frame, text="Mark as Completed", width=20, command=mark_completed)
mark_completed_button.grid(row=1, column=1, padx=5)

edit_task_button = tk.Button(frame, text="Edit Task", width=20, command=edit_task)
edit_task_button.grid(row=2, column=0, padx=5, pady=5)

clear_button = tk.Button(frame, text="Clear All", width=20, command=clear_all)
clear_button.grid(row=2, column=1, padx=5, pady=5)

task_listbox = tk.Listbox(frame, width=50, height=15)
task_listbox.grid(row=3, column=0, columnspan=2, pady=10)

# Populate the Listbox with loaded tasks
for task in tasks:
    task_listbox.insert(tk.END, task)

# Run the main event loop
root.mainloop()
