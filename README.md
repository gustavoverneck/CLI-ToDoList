[# CLI-ToDoList
A command line to-do list.
](https://roadmap.sh/projects/task-tracker)

# Todoi

A command-line interface (CLI) for managing tasks. The task manager allows you to perform various actions like adding, removing, updating, and marking tasks as complete, incomplete, or in progress. It also lets you export tasks and display filtered task lists based on their status.

## Features

- Add a task
- List all tasks
- Remove a task by index
- Update a task's description
- Mark a task as complete, incomplete, or in progress
- List tasks filtered by status (complete, incomplete, progress)
- Export tasks to a file
- Help command with descriptions of available commands

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gustavoverneck/Todoi

2. Run the folder
   ```bash
   python3 todoi

3. (Optional) Add bash alias
  ```bash
  echo 'alias todoi="python3 ~/path/to/Todoi"' >> ~/.bashrc  # or ~/.zshrc for Zsh ir ~/.config/fish/condig.fish for fish
  source ~/.bashrc  # Apply changes

## Usage

Run the script with commands:

```bash
python3 __main__.py [command] [arguments]

or if you set up an alias:

```bash
todoi [command] [arguments]
