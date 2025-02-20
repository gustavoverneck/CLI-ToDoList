# Task manager CLI

# Imports
import argparse
import os
import json

# --------------------------------------------

class TaskManager:
    def __init__(self):
        self.create_parser() # Create parser
        self.args = self.parser.parse_args() # Parse arguments
        self.tasks = [] # List containing all tasks
        self.tasks_dir = "tasks.json"
        self.checkFile()
        self.read_from_file()
        self.update_tasks_id()
        self.execute_command()
        
    def checkFile(self):
        if not os.path.exists(self.tasks_dir):
            with open(self.tasks_dir, "w") as f:
                json.dump([], f)
    
    def update_tasks_id(self):
        for i in range(len(self.tasks)):
            self.tasks[i]["id"] = i + 1
            
    def interpret_input(self):
        num_words = len(self.input_line.split(" "))
        if num_words == 0:
            print("Invalid command. Type 'help' for a list of commands.")
            return
                
        self.input_command = self.input_line.split(" ")[0] # Get first word of input
        if self.input_command not in self.valid_commands:
            print("Invalid command. Type 'help' for a list of commands.")
        
        self.execute_command()  # Execute command
    
    def execute_command(self):
        if self.args.add:
            self.cmd_add()
        elif self.args.list:
            self.cmd_list()
        elif self.args.remove:
            self.cmd_remove()
        elif self.args.update:
            self.cmd_update()
        elif self.args.complete:
            self.cmd_mark_complete()
        elif self.args.incomplete:
            self.cmd_mark_incomplete()
        elif self.args.progress:
            self.cmd_mark_progress()
        else:
            self.cmd_help()
    
    def cmd_help(self):
        print("Commands:")
        print("add <task> - Add a new task")
        print("help - Display this message")
        print("list - List all tasks")
        print("q - Quit program")

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
        id = len(self.tasks) + 1
        description = self.args.add
        task = {"id": id, "description": description, "status": "incomplete"}
        self.tasks.append(task)
        self.export_tasks()
        print(f"Task '{task["description"]}' added with id '{id}'.")
    
    def cmd_quit(self):
        self.running = False
    
    def cmd_mark_complete(self):
        index = int(self.args.complete) - 1
        self.tasks[index]["status"] = "complete"
        self.export_tasks()
        print(f"Task {index + 1} marked as complete.")
    
    def cmd_mark_incomplete(self):
        index = int(self.args.incomplete) - 1
        self.tasks[index]["status"] = "incomplete"
        self.export_tasks()
        print(f"Task {index + 1} marked as incomplete.")
    
    def cmd_mark_progress(self):
        index = int(self.args.progress) - 1
        self.tasks[index]["status"] = "in progress"
        self.export_tasks()
        print(f"Task {index + 1} marked as in progress.")

    def export_tasks(self):
        self.update_tasks_id()
        with open(self.tasks_dir, "w") as f:
            json.dump({"tasks": self.tasks}, f)
    
    def read_from_file(self):
        with open(self.tasks_dir, "r") as f:
            self.json_tasks = json.load(f)
        self.tasks = self.json_tasks["tasks"]
    
    def cmd_remove(self):
        index = int(self.args.remove) - 1
        task = self.tasks.pop(index)
        self.export_tasks()
        print(f"Task {task['id']} removed.")
    
    def cmd_update(self):
        index = int(self.args.update) - 1
        task = self.tasks[index]
        new_description = input("Enter new description: ")
        task["description"] = new_description
        self.export_tasks()
        print(f"Task {task['id']} updated.")

    def create_parser(self):
        self.parser = argparse.ArgumentParser(description="Task Tracker CLI")
        self.parser.add_argument("-a", "--add", metavar="", help="Add a new task")
        self.parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
        self.parser.add_argument("-r", "--remove", metavar="", help="Remove a task by index")
        self.parser.add_argument("-u", "--update", metavar="", help="Update a task by index")
        self.parser.add_argument("-c", "--complete", metavar="", help="Mark a task as complete")
        self.parser.add_argument("-i", "--incomplete", metavar="", help="Mark a task as incomplete")
        self.parser.add_argument("-p", "--progress", metavar="", help="Mark a task as in progress")


# --------------------------------------------
# Main
if __name__ == '__main__':
    app = TaskManager()
