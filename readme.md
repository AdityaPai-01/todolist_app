# PyLISTS Todo-List Application

## Project Overview

PyLISTS is a Python command-line todo-list application CRUD CLI. Users can register or log in, organize tasks into named lists, and save their data locally between runs.

## ⚠️ IMPORTANT NOTE ⚠️
I have used Artificial Intelligence (AI) to help me build this project, in following ways:
- To write boilerplate/repeated code, without making any design structure changes
- To help me understand the problems better, in-case I am unable to get a clear picture of it
- Help me draft solutions by recommendations, ask questions to it about the decisions I plan to make and review it

The main objective of this project is to learn how to integrate different systems efficiently, and to learn to build and learn with AI, and not about letting AI do all the work instead.

## Features

- Register an account and log in.
- Create, rename, delete, and switch between task lists.
- Add, view, rename, and delete tasks.
- Add or update a task's description and filter text.
- Mark tasks as complete or pending.
- Choose a display theme and default list.
- Change a username or delete an account.

## Technologies Used

- Python
- [Rich](https://pypi.org/project/rich/) for styled terminal output and prompts
- Python standard-library modules, including `json`, `pathlib`, `logging`, and `uuid`

## Installation and Setup

1. Install Python.
2. From the project root, install the dependency:

   ```shell
   python -m pip install -r requirements.txt
   ```

3. Start the application from the project root:

   ```shell
   python src\main.py
   ```

## Usage

On launch, choose `R` to register or `L` to log in. After logging in, enter `!hp` at the task manager prompt to see the available commands.

Use the commands to manage tasks and lists. The `!us` command opens user settings; enter `!ex` there to return to the task manager. Use `!ex` at the task manager prompt to exit.

## Project Structure

```text
data/                       Local JSON data and application log
src/
  main.py                   Application entry point and initialization
  logging_config.py         Logging setup
  interface/
    tdl_interface.py        Task and list command-line interface
    ul_interface.py         Login, registration, and user settings
  manager/
    data_manager.py         JSON file loading and saving
    list_manager.py         Task-list operations
    task_manager.py         Task operations
    user_manager.py         Account operations
  model/
    task.py                 Task data model
    user.py                 User data model
requirements.txt            External Python dependency
```

## Data Storage

The application stores data in JSON files under `data/`. Account data is stored in `data/user_data.json`; each user's task lists are stored in that user's directory as `list_data.json`. The application creates missing data directories and files as needed, and writes a log to `data/log_data.log`.

## Limitations

- If JSON data is invalid or unreadable, loading reports a failure. The application does not automatically repair the file, and corrupted account data may not be handled consistently.
- Account passwords are stored as plain text in the account JSON file. Do not use real or sensitive passwords with this project.
- Password changes are not implemented.
