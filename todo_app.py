import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import json

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the title  and size of the window 
        self.title("Todo List App")
        self.geometry("600x600")  # Set the window size to  600x600

        # Apply ttkbootstrap theme
        style = Style(theme="flatly")
        style.configure("Custon.TEntry", foreground="gray")

        # create input field for adding tasks
        self.task_input = ttk.Entry(self, font=("TkdefaultFont", 16), width=30, style="Custon.TEntry")
        self.task_input.pack(pady=10)

        # set placeholder for input field 
        self.task_input.insert(0, "Enter your todo here...")

        # Bind event to clear placeholder when input field is clicked 
        self.task_input.bind("<FocusIn>", self.clear_placeholder)

        # for w restore when use lose focus
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        # create button for adding tasks
        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        # create listbox to display tasks
        self.task_list = tk.Listbox(self, font=("TkDefaultFont", 20), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # create buttons for Done or deleting the task 
        ttk.Button(self, text="Done", style="Success.TButton", command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", style="danger.TButton", command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)
        
        # create button for displaying task statistics 
        ttk.Button(self, text="View Stats", style="info.TButton", command=self.view_stats).pack(side=tk.BOTTOM, pady=10)
        
        # Load tasks when the app starts
        self.load_tasks()

    # function to clear the placeholder
    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter your todo here...":
            self.task_input.delete(0, tk.END)
            self.task_input.configure(style='TEntry')

    # Function to restore the placeholder 
    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")
            self.task_input.configure(style="TEntry")

    # adding task functionality
    def add_task(self):
        task = self.task_input.get()
        if task and task != "Enter your todo here...":
            self.task_list.insert(tk.END, task)  # add task to listbox
            self.task_list.itemconfig(tk.END, fg="orange")  # new tasks are orange color
            self.task_input.delete(0, tk.END)  # clear input field
            self.save_tasks()  # save tasks to file 
        else:
            messagebox.showwarning("Input Error", "please enter a valid task ")

    # implementing mark and delete function
    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            self.save_tasks()

    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.delete(task_index)
            self.save_tasks()

    # implementing the stats function
    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1 
        messagebox.showinfo("Task statistics", f"Total tasks: {total_count}\ncompleted tasks: {done_count}")

    # saving the tasks in JSON file format 
    def save_tasks(self):
        data = []
        for i in range(self.task_list.size()):
            text = self.task_list.get(i)
            color = self.task_list.itemcget(i, "fg")
            data.append({"text": text, "color": color})
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    # loading the task from file 
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)  # Fix typo from 'laod' to 'load'
                for task in data:
                    self.task_list.insert(tk.END, task["text"])  # Corrected key to 'text'
                    self.task_list.itemconfig(tk.END, fg=task["color"])
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()
