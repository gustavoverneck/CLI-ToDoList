# Task manager CLI

# Imports
import sys
import os
import json

# --------------------------------------------

def custom_excepthook(exctype, value, traceback):   # Custom excepthook function
    print(f"Error: {value}")  # Prints only the error message

sys.excepthook = custom_excepthook  # Set custom excepthook for more readable error messages

# --------------------------------------------

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure self.tasks_dir uses the correct path
tasks_dir = os.path.join(script_dir, "tasks.json")  # Adjust the filename as needed
    

class TaskManager:
    def __init__(self):
        self.valid_commands = ["add", "list", "remove", "update", "complete", "incomplete", "progress", "list-complete", "list-incomplete", "list-progress", "export", "help"]
        self.short_commands = ["-a", "-l", "-r", "-u", "-c", "-i", "-p", "-lc", "-li", "-lp", "-e", "-h"]
        self.tasks = [] # List containing all tasks
        self.tasks_dir = tasks_dir # Path to the tasks file
        self.checkFile()    # Check if file exists
        self.read_from_file()   # Read tasks from file
        self.update_tasks_id()  # Update tasks id
        self.create_parser() # Create parser
        
    def checkFile(self):
        if not os.path.exists(self.tasks_dir):
            with open(self.tasks_dir, "w") as f:
                json.dump([], f)
    
    def update_tasks_id(self):
        for i in range(len(self.tasks)):
            self.tasks[i]["id"] = i + 1
    
    def cmd_help(self):
        print("Commands:")
        print("-a add - Add a new task")
        print("-a list - List all tasks")
        print("-r remove - Remove a task by index")
        print("-u update - Update a task by index")
        print("-c complete - Mark a task as complete")
        print("-i incomplete - Mark a task as incomplete")
        print("-p progress - Mark a task as in progress")
        print("-lc list-complete - List all complete tasks")
        print("-li list-incomplete - List all incomplete tasks")
        print("-lp list-progress - List all tasks in progress")
        print("-e export - Export tasks to file")
        print("-h help - Display help message")

    def cmd_list(self):
        if len(self.tasks) == 0:
            print("No tasks.")
        else:
            print("-" * 29)
            print("| id | description | status |")
            print("-" * 29)
            for task in self.tasks:
                print(f"{task['id']} | {task['description']} | {task['status']}")

    def cmd_add(self):
        # Check if description is provided
        if len(self.args) == 0:
            raise ValueError("No description provided.")
        self.args = self.args[0]
        id = len(self.tasks) + 1
        description = self.args
        task = {"id": id, "description": description, "status": "incomplete"}
        self.tasks.append(task)
        self.export_tasks()
        print(f"Task '{task["description"]}' added with id '{id}'.")
    
    def cmd_mark_complete(self):
        # Check if index is provided
        if len(self.args) == 0:
            raise ValueError("No index provided.")
        self.args = self.args[0]
        if not self.args.isdigit():
            raise ValueError("Index must be an integer.")
        if int(self.args) > len(self.tasks):
            raise ValueError("Index out of range.")
        index = int(self.args) - 1
        self.tasks[index]["status"] = "complete"
        self.export_tasks()
        print(f"Task {index + 1} marked as complete.")
    
    def cmd_mark_incomplete(self):
        # Check if index is provided
        if len(self.args) == 0:
            raise ValueError("No index provided.")
        self.args = self.args[0]
        if not self.args.isdigit():
            raise ValueError("Index must be an integer.")
        if int(self.args) > len(self.tasks):
            raise ValueError("Index out of range.")
        index = int(self.args) - 1
        self.tasks[index]["status"] = "incomplete"
        self.export_tasks()
        print(f"Task {index + 1} marked as incomplete.")
    
    def cmd_mark_progress(self):
        # Check if index is provided
        if len(self.args) == 0:
            raise ValueError("No index provided.")
        self.args = self.args[0]
        if not self.args.isdigit():
            raise ValueError("Index must be an integer.")
        if int(self.args) > len(self.tasks):
            raise ValueError("Index out of range.")
        index = int(self.args) - 1
        self.tasks[index]["status"] = "in progress"
        self.export_tasks()
        print(f"Task {index + 1} marked as in progress.")

    def export_tasks(self):
        self.update_tasks_id()
        with open(self.tasks_dir, "w") as f:
            json.dump({"tasks": self.tasks}, f)
    
    def read_from_file(self):
        try:
            with open(self.tasks_dir, "r") as f:
                self.json_tasks = json.load(f)
            
            # If the JSON is a list, assume it's the task list
            if isinstance(self.json_tasks, list):
                self.tasks = self.json_tasks
            elif isinstance(self.json_tasks, dict) and "tasks" in self.json_tasks:
                self.tasks = self.json_tasks["tasks"]
            else:
                print("Error: Unexpected JSON format.")
                self.tasks = []
        except FileNotFoundError:
            print(f"Error: The file {self.tasks_dir} was not found.")
            self.tasks = []
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON from {self.tasks_dir}.")
            self.tasks = []
    
    def cmd_remove(self):
        # Check if index is provided
        if len(self.args) == 0:
            raise ValueError("No index provided.")
        self.args = self.args[0]
        if not self.args.isdigit():
            raise ValueError("Index must be an integer.")
        if int(self.args) > len(self.tasks):
            raise ValueError("Index out of range.")
        index = int(self.args) - 1
        task = self.tasks.pop(index)
        self.export_tasks()
        print(f"Task {task['id']} removed.")
    
    def cmd_update(self):
        # Check if index is provided
        if len(self.args) == 0:
            raise ValueError("No index provided.")
        if not self.args.isdigit():
            raise ValueError("Index must be an integer.")
        if int(self.args) > len(self.tasks):
            raise ValueError("Index out of range.")
        self.args = self.args[0]
        index = int(self.args) - 1
        task = self.tasks[index]
        new_description = input("Enter new description: ")
        task["description"] = new_description
        self.export_tasks()
        print(f"Task {task['id']} updated.")
    
    def cmd_list_complete(self):
        for task in self.tasks:
            if task["status"] == "complete":
                print(f"{task['id']} | {task['description']} | {task['status']}")
    
    def cmd_list_incomplete(self):
        for task in self.tasks:
            if task["status"] == "incomplete":
                print(f"{task['id']} | {task['description']} | {task['status']}")
    
    def cmd_list_progress(self):
        for task in self.tasks:
            if task["status"] == "in progress":
                print(f"{task['id']} | {task['description']} | {task['status']}")
    
    def cmd_export(self):
        self.export_tasks()
        print("Tasks exported to file.")

    def create_parser(self):
        if len(sys.argv[1]) > 0:
            self.input_line = sys.argv[1]
            self.args = sys.argv[2:]
        else:
            raise ValueError("No arguments provided.")
    
        if self.input_line == "-a" or self.input_line == "add":
            self.cmd_add()
        elif self.input_line == "-l" or self.input_line == "list":
            self.cmd_list()
        elif self.input_line == "-r" or self.input_line == "remove":
            self.cmd_remove()
        elif self.input_line == "-u" or self.input_line == "update":
            self.cmd_update()
        elif self.input_line == "-c" or self.input_line == "complete":
            self.cmd_mark_complete()
        elif self.input_line == "-i" or self.input_line == "incomplete":
            self.cmd_mark_incomplete()
        elif self.input_line == "-p" or self.input_line == "progress":
            self.cmd_mark_progress()
        elif self.input_line == "-lc" or self.input_line == "list-complete":
            self.cmd_list_complete()
        elif self.input_line == "-li" or self.input_line == "list-incomplete":
            self.cmd_list_incomplete()
        elif self.input_line == "-lp" or self.input_line == "list-progress":
            self.cmd_list_progress()
        elif self.input_line == "-e" or self.input_line == "export":
            self.cmd_export()
        elif self.input_line == "-h" or self.input_line == "help":
            self.cmd_help()
        else:
            raise ValueError("Invalid command.")

# --------------------------------------------
# Main
if __name__ == '__main__':
    app = TaskManager()