"""
Todo Backend - Core functionality for task management.

This module handles CRUD operations and CSV persistence for a to-do list application.
It maintains an in-memory task list that syncs with a CSV file for data persistence.

Module-level variables:
    tasks (list): Global list of task dictionaries
    next_id (int): Counter for generating unique task IDs
"""

import csv
import os

# Global state
tasks = []
next_id = 0


def get_tasks():
    """
    Load tasks from CSV file into memory.
    
    Reads all tasks from 'tasks.csv' and populates the global tasks list.
    Creates the CSV file with headers if it doesn't exist. Updates the
    next_id counter to ensure unique IDs for new tasks.
    
    Side effects:
        - Modifies global 'tasks' list
        - Modifies global 'next_id' counter
        - Creates 'tasks.csv' if it doesn't exist
    
    Returns:
        None
    """
    global next_id, tasks

    # Reset tasks list to avoid duplicates on subsequent calls
    tasks = []
    
    # Create CSV with headers if it doesn't exist
    if not os.path.exists("tasks.csv"):
        with open("tasks.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "task", "description", "completion_status"])
    else:
        # Load existing tasks from CSV
        with open("tasks.csv") as file:
            reader = csv.DictReader(file)
            for task in reader:
                # Convert string values to appropriate types
                task["id"] = int(task["id"])
                task["completion_status"] = (task["completion_status"] == "True")
                tasks.append(task)

    # Set next_id to one greater than highest existing ID to avoid conflicts
    if tasks:
        next_id = max(tasks, key=lambda task: task["id"])["id"] + 1


def add_task(task_name, description=""):
    """
    Add a new task to the list and persist to CSV.
    
    Creates a new task with a unique ID and default incomplete status.
    Only adds the task if task_name is not empty.
    
    Args:
        task_name (str): The task name/title (required)
        description (str): Optional description/details for the task
    
    Side effects:
        - Appends to global 'tasks' list
        - Increments global 'next_id'
        - Writes to 'tasks.csv'
    
    Returns:
        None
    """
    global tasks, next_id
    
    # Validate task name exists before adding
    if task_name:
        tasks.append({
            "id": next_id,
            "task": task_name,
            "description": description,
            "completion_status": False,
        })
        # Increment ID only after successful addition
        next_id += 1
        save_tasks()


def delete_task(task_id, flag=None):
    """
    Delete a task by its ID and persist changes.
    
    Removes the task with the specified ID from the tasks list.
    If flag is provided (typically "All"), clears all tasks from CSV first.
    
    Args:
        task_id (int): The unique identifier of the task to delete
        flag (str, optional): Special flag for batch operations (e.g., "All")
    
    Side effects:
        - Removes task from global 'tasks' list
        - Writes to 'tasks.csv'
    
    Returns:
        None
    """
    global tasks
    
    # If flag is provided, clear the CSV (used for "Delete All" functionality)
    if flag:
        with open("tasks.csv", "w", newline="") as file:
            fieldnames = ["id", "task", "description", "completion_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        tasks = []
        return

    # Search for task with matching ID and remove it
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks()
            return


def mark_task_complete(task_id):
    """
    Mark a task as complete by its ID and persist changes.
    
    Sets the completion_status of the specified task to True.
    
    Args:
        task_id (int): The unique identifier of the task to mark complete
    
    Side effects:
        - Modifies task in global 'tasks' list
        - Writes to 'tasks.csv'
    
    Returns:
        None
    """
    global tasks

    # Find task and update completion status
    for task in tasks:
        if task["id"] == task_id:
            task["completion_status"] = True
            save_tasks()
            return


def edit_task(task_id, new_name=None, new_description=None):
    """
    Edit a task's name and/or description and persist changes.
    
    Updates the specified fields of a task. At least one field must be provided.
    Empty strings are treated as valid updates.
    
    Args:
        task_id (int): The unique identifier of the task to edit
        new_name (str, optional): New task name
        new_description (str, optional): New description
    
    Side effects:
        - Modifies task in global 'tasks' list
        - Writes to 'tasks.csv'
    
    Returns:
        None
    """
    global tasks

    # Validate at least one field is being updated
    if new_name is None and new_description is None:
        return

    # Find task and update provided fields
    for task in tasks:
        if task["id"] == task_id:
            if new_name is not None:
                task["task"] = new_name
            if new_description is not None:
                task["description"] = new_description
            save_tasks()
            return


def save_tasks():
    """
    Save all tasks from memory to the CSV file.
    
    Overwrites the entire CSV file with current task data from memory.
    Uses DictWriter to maintain consistent field ordering.
    
    Side effects:
        - Overwrites 'tasks.csv' with current task data
    
    Returns:
        None
    
    Note:
        newline="" parameter prevents extra blank lines on Windows
    """
    with open("tasks.csv", "w", newline="") as file:
        fieldnames = ["id", "task", "description", "completion_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)