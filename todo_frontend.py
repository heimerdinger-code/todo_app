"""
Todo Frontend - GUI interface for the todo list application.

Built with CustomTkinter for a modern, user-friendly interface.
Provides Add, Edit, Delete, and Complete functionality with modal views.
Works in conjunction with todo_backend.py for data persistence.
"""

import customtkinter
import todo_backend

# Color scheme for hover effects
HOVER_COLOR = "#1f538d"  # Darker blue for button hover
BUTTON_COLOR = "#1f6aa5"  # Default button color


def main():
    """
    Application entry point.
    
    Creates the main window, initializes the UI, and starts the event loop.
    
    Returns:
        None
    """
    app = customtkinter.CTk()
    create_window(app)
    app.mainloop()


def create_title(app):
    """
    Create and display the application title bar.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Sets the window title
        - Adds a bold title label at the top of the window
    
    Returns:
        None
    """
    app.title("To-Do List App")
    label_text = customtkinter.CTkLabel(
        master=app, 
        text="To-Do List App", 
        font=("Arial", 24, "bold")
    )
    label_text.pack(pady=20)


def create_list(app):
    """
    Load and display all tasks in a scrollable frame.
    
    Reloads tasks from backend to ensure fresh data, then creates
    a scrollable frame displaying each task with completion indicator.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Reloads tasks from backend
        - Creates scrollable frame and stores reference in app.scrollable_frame
        - Displays each task with completion indicator (✓) and truncated text
    
    Returns:
        None
    """
    # Reload tasks from CSV to ensure fresh data
    todo_backend.get_tasks()

    # Create a scrollable frame for task list
    scrollable_frame = customtkinter.CTkScrollableFrame(
        app, 
        width=250, 
        height=200
    )
    scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Store reference for later access (needed when switching modes)
    app.scrollable_frame = scrollable_frame
    
    # Display each task with completion indicator
    for task in todo_backend.tasks:
        # Add checkmark prefix for completed tasks
        prefix = "✓ " if task["completion_status"] else ""
        
        # Format display text based on whether description exists
        if task["description"]:
            display_text = (
                f'{prefix}{truncate(task["task"], 10)} - '
                f'{truncate(task["description"], 25)}'
            )
        else:
            # No description - just show task name
            display_text = f'{prefix}{truncate(task["task"], 15)}'
        
        label = customtkinter.CTkLabel(
            scrollable_frame, 
            text=display_text
        )
        label.pack(pady=5, padx=10, anchor="w")


def truncate(text, max_length):
    """
    Truncate text to maximum length, adding ellipsis if shortened.
    
    Args:
        text (str): The string to potentially truncate
        max_length (int): Maximum allowed character length
    
    Returns:
        str: Original text if under limit, otherwise truncated text with "..."
    
    Example:
        >>> truncate("Buy groceries from store", 15)
        'Buy groceries...'
    """
    if len(text) > max_length:
        return f"{text[:max_length-3]}..."
    return text


def create_buttons(app):
    """
    Create the 2x2 grid of action buttons (Add, Complete, Delete, Edit).
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Creates button frame and stores reference in app.button_frame
        - Creates four action buttons with hover effects
    
    Returns:
        None
    """
    button_frame = customtkinter.CTkFrame(app)
    button_frame.pack(pady=20)

    # Store reference so it can be hidden/shown when switching modes
    app.button_frame = button_frame

    # Add button
    add_button = customtkinter.CTkButton(
        button_frame, 
        text="Add", 
        command=lambda: add_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    add_button.grid(row=0, column=0, padx=5, pady=5)

    # Complete button
    complete_button = customtkinter.CTkButton(
        button_frame, 
        text="Complete", 
        command=lambda: complete_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    complete_button.grid(row=0, column=1, padx=5, pady=5)

    # Delete button
    delete_button = customtkinter.CTkButton(
        button_frame, 
        text="Delete", 
        command=lambda: delete_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    delete_button.grid(row=1, column=0, padx=5, pady=5)

    # Edit button
    edit_button = customtkinter.CTkButton(
        button_frame, 
        text="Edit", 
        command=lambda: edit_select_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    edit_button.grid(row=1, column=1, padx=5, pady=5)


def create_window(app):
    """
    Orchestrate initial UI setup by creating all components in order.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Creates title, task list, and action buttons
    
    Returns:
        None
    
    Note:
        Order matters - title, then list, then buttons creates proper layout
    """
    create_title(app)
    create_list(app)
    create_buttons(app)


def add_mode(app):
    """
    Switch from Normal mode to Add mode.
    
    Displays input fields for creating a new task with Submit and Cancel options.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Hides normal mode UI elements
        - Creates Add mode frame with entry fields
        - Stores references to entry fields in app for submission handler
    
    Returns:
        None
    """
    hide_normal_mode(app)
    
    # Create frame for Add mode interface
    add_frame = customtkinter.CTkFrame(app, width=250, height=200)
    add_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Store reference for cleanup when returning to Normal mode
    app.current_frame = add_frame

    # Title label
    label_text = customtkinter.CTkLabel(
        master=add_frame, 
        text="Add Task", 
        font=("Arial", 20, "bold")
    )
    label_text.pack(pady=20)

    # Task name input field
    task_entry = customtkinter.CTkEntry(
        add_frame, 
        placeholder_text='Task: [e.g., "Buy groceries"]'
    )
    task_entry.pack(pady=20, padx=20, fill="x", expand=True)

    # Store reference so Submit button can retrieve entered text
    app.add_task_entry = task_entry

    # Description input field (optional)
    desc_entry = customtkinter.CTkEntry(
        add_frame, 
        placeholder_text='Description: [e.g., "From store"]'
    )
    desc_entry.pack(pady=20, padx=20, fill="x", expand=True)

    # Store reference for submission
    app.add_desc_entry = desc_entry

    # Create button container for Submit and Cancel
    add_button_frame = customtkinter.CTkFrame(add_frame)
    add_button_frame.pack(pady=20)

    # Submit button - process the new task
    add_button = customtkinter.CTkButton(
        add_button_frame, 
        text="Add", 
        command=lambda: handle_add_submit(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    add_button.grid(row=0, column=0, padx=5, pady=5)

    # Cancel button - return to Normal mode without saving
    cancel_button = customtkinter.CTkButton(
        add_button_frame, 
        text="Cancel", 
        command=lambda: show_normal_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    cancel_button.grid(row=0, column=1, padx=5, pady=5)


def handle_add_submit(app):
    """
    Process new task submission from Add mode.
    
    Validates that task name is not empty, then adds to backend.
    Shows error popup if validation fails.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Calls backend to add task if valid
        - Returns to Normal mode, refreshing the task list
        - Shows error popup if task name is empty
    
    Returns:
        None
    """
    # Validate task name is not empty
    if not app.add_task_entry.get().strip():
        show_popup(app, "Can't add task without name")
        return

    # Add task to backend
    todo_backend.add_task(
        app.add_task_entry.get().strip(), 
        app.add_desc_entry.get().strip()
    )

    # Return to Normal mode with updated task list
    show_normal_mode(app)


def edit_select_mode(app):
    """
    Switch to Edit Select mode to choose which task to edit.
    
    Displays radio buttons for all tasks. User selects one to proceed to edit form.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Hides normal mode UI elements
        - Creates selection interface with radio buttons
        - Shows error popup if no tasks exist
    
    Returns:
        None
    """
    # Check if there are any tasks to edit
    if not todo_backend.tasks:
        show_popup(app, "No tasks available to edit")
        return
    
    hide_normal_mode(app)

    # Create frame for Edit select mode interface
    edit_select_frame = customtkinter.CTkFrame(app, width=250, height=200)
    edit_select_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Store reference for cleanup when returning to Normal mode
    app.current_frame = edit_select_frame

    # Title label
    label_text = customtkinter.CTkLabel(
        master=edit_select_frame, 
        text="Select Task", 
        font=("Arial", 20, "bold")
    )
    label_text.pack(pady=20)

    # Create variable to track selection (-1 means no selection)
    selected_var = customtkinter.IntVar(value=-1)

    # Store it so Next button can access it later
    app.selected_edit_var = selected_var

    # Create radio button for each task
    for task in todo_backend.tasks:
        radio = customtkinter.CTkRadioButton(
            edit_select_frame,
            text=task["task"],
            variable=selected_var,
            value=task["id"]
        )
        radio.pack(pady=5, padx=10, anchor="w")

    # Create button container for Next and Cancel
    edit_select_button_frame = customtkinter.CTkFrame(edit_select_frame)
    edit_select_button_frame.pack(pady=20)

    # Next button - proceed to edit form
    next_button = customtkinter.CTkButton(
        edit_select_button_frame, 
        text="Next", 
        command=lambda: edit_form_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    next_button.grid(row=0, column=0, padx=5, pady=5)

    # Cancel button - return to Normal mode without editing
    cancel_button = customtkinter.CTkButton(
        edit_select_button_frame, 
        text="Cancel", 
        command=lambda: show_normal_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    cancel_button.grid(row=0, column=1, padx=5, pady=5)


def edit_form_mode(app):
    """
    Switch to Edit Form mode to modify the selected task.
    
    Pre-fills form fields with current task data for editing.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Destroys selection frame
        - Creates edit form with pre-filled data
        - Shows error popup if no task was selected
    
    Returns:
        None
    """
    # Validate that a task was selected
    if app.selected_edit_var.get() == -1:
        show_popup(app, "Please select a task first")
        return
    
    # Clean up selection frame
    app.current_frame.destroy()

    # Find the selected task
    selected_id = app.selected_edit_var.get()
    app.edit_task_id = selected_id

    selected_task = None
    for task in todo_backend.tasks:
        if task["id"] == selected_id:
            selected_task = task
            break

    # Create frame for Edit mode interface
    edit_form_frame = customtkinter.CTkFrame(app, width=250, height=200)
    edit_form_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Store reference for cleanup when returning to Normal mode
    app.current_frame = edit_form_frame

    # Title label
    label_text = customtkinter.CTkLabel(
        master=edit_form_frame, 
        text="Edit Task", 
        font=("Arial", 20, "bold")
    )
    label_text.pack(pady=20)

    # Task name edit field (pre-filled with current value)
    task_edit_entry = customtkinter.CTkEntry(edit_form_frame)
    task_edit_entry.pack(pady=20, padx=20, fill="x", expand=True)
    task_edit_entry.insert(0, selected_task["task"])
    
    # Store reference so Submit button can retrieve entered text
    app.edit_task_entry = task_edit_entry

    # Description edit field (pre-filled with current value)
    desc_edit_entry = customtkinter.CTkEntry(edit_form_frame)
    desc_edit_entry.pack(pady=20, padx=20, fill="x", expand=True)
    desc_edit_entry.insert(0, selected_task["description"])

    # Store reference for submission
    app.edit_desc_entry = desc_edit_entry

    # Create button container for Submit and Cancel
    edit_form_button_frame = customtkinter.CTkFrame(edit_form_frame)
    edit_form_button_frame.pack(pady=20)

    # Submit button - save changes
    submit_button = customtkinter.CTkButton(
        edit_form_button_frame, 
        text="Edit", 
        command=lambda: handle_edit_submit(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    submit_button.grid(row=0, column=0, padx=5, pady=5)

    # Cancel button - return to Normal mode without saving
    cancel_button = customtkinter.CTkButton(
        edit_form_button_frame, 
        text="Cancel", 
        command=lambda: show_normal_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    cancel_button.grid(row=0, column=1, padx=5, pady=5)


def handle_edit_submit(app):
    """
    Process task edit submission.
    
    Validates that task name is not empty, then updates backend.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Calls backend to update task if valid
        - Returns to Normal mode, refreshing the task list
        - Shows error popup if task name is empty
    
    Returns:
        None
    """
    # Validate task name is not empty
    if not app.edit_task_entry.get().strip():
        show_popup(app, "Task name cannot be empty")
        return
    
    # Update task in backend
    todo_backend.edit_task(
        app.edit_task_id, 
        app.edit_task_entry.get(), 
        app.edit_desc_entry.get()
    )

    # Return to Normal mode with updated task list
    show_normal_mode(app)


def complete_mode(app):
    """
    Switch to Complete mode to mark a task as done.
    
    Displays radio buttons for all incomplete tasks.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Hides normal mode UI elements
        - Creates selection interface with radio buttons for incomplete tasks
        - Shows error popup if no tasks exist
    
    Returns:
        None
    """
    # Check if there are any tasks to complete
    if not todo_backend.tasks:
        show_popup(app, "No tasks available to complete")
        return
    
    hide_normal_mode(app)

    # Create frame for Complete mode interface
    complete_frame = customtkinter.CTkFrame(app, width=250, height=200)
    complete_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Store reference for cleanup when returning to Normal mode
    app.current_frame = complete_frame

    # Title label
    label_text = customtkinter.CTkLabel(
        master=complete_frame, 
        text="Complete Task", 
        font=("Arial", 20, "bold")
    )
    label_text.pack(pady=20)

    # Create variable to track selection (-1 means no selection)
    selected_var = customtkinter.IntVar(value=-1)

    # Store it so Complete button can access it later
    app.selected_complete_var = selected_var

    # Create radio button for each incomplete task
    for task in todo_backend.tasks:
        if not task["completion_status"]:
            radio = customtkinter.CTkRadioButton(
                complete_frame,
                text=task["task"],
                variable=selected_var,
                value=task["id"]
            )
            radio.pack(pady=5, padx=10, anchor="w")

    # Create button container for Complete and Cancel
    complete_button_frame = customtkinter.CTkFrame(complete_frame)
    complete_button_frame.pack(pady=20)

    # Complete button - mark task as done
    complete_button = customtkinter.CTkButton(
        complete_button_frame, 
        text="Complete", 
        command=lambda: handle_complete_submit(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    complete_button.grid(row=0, column=0, padx=5, pady=5)

    # Cancel button - return to Normal mode without changes
    cancel_button = customtkinter.CTkButton(
        complete_button_frame, 
        text="Cancel", 
        command=lambda: show_normal_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    cancel_button.grid(row=0, column=1, padx=5, pady=5)


def handle_complete_submit(app):
    """
    Process task completion.
    
    Marks the selected task as complete in the backend.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Calls backend to mark task complete if valid
        - Returns to Normal mode, refreshing the task list
        - Shows error popup if no task was selected
    
    Returns:
        None
    """
    # Validate that a task was selected
    if app.selected_complete_var.get() == -1:
        show_popup(app, "Please select a task first")
        return
    
    # Mark task as complete in backend
    todo_backend.mark_task_complete(app.selected_complete_var.get())

    # Return to Normal mode with updated task list
    show_normal_mode(app)


def delete_mode(app):
    """
    Switch to Delete mode to remove a task.
    
    Displays radio buttons for all tasks with Delete and Delete All options.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Hides normal mode UI elements
        - Creates selection interface with radio buttons for all tasks
        - Shows error popup if no tasks exist
    
    Returns:
        None
    """
    # Check if there are any tasks to delete
    if not todo_backend.tasks:
        show_popup(app, "No tasks available to delete")
        return
    
    hide_normal_mode(app)

    # Create frame for Delete mode interface
    delete_frame = customtkinter.CTkFrame(app, width=250, height=200)
    delete_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Store reference for cleanup when returning to Normal mode
    app.current_frame = delete_frame

    # Title label
    label_text = customtkinter.CTkLabel(
        master=delete_frame, 
        text="Delete Task", 
        font=("Arial", 20, "bold")
    )
    label_text.pack(pady=20)

    # Create variable to track selection (-1 means no selection)
    selected_var = customtkinter.IntVar(value=-1)

    # Store it so Delete button can access it later
    app.selected_delete_var = selected_var

    # Create radio button for each task
    for task in todo_backend.tasks:
        radio = customtkinter.CTkRadioButton(
            delete_frame,
            text=task["task"],
            variable=selected_var,
            value=task["id"]
        )
        radio.pack(pady=5, padx=10, anchor="w")

    # Create button container for Delete, Cancel, and Delete All
    delete_button_frame = customtkinter.CTkFrame(delete_frame)
    delete_button_frame.pack(pady=20)

    # Delete button - remove selected task
    delete_button = customtkinter.CTkButton(
        delete_button_frame, 
        text="Delete", 
        command=lambda: handle_delete_submit(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    delete_button.grid(row=0, column=0, padx=5, pady=5)

    # Cancel button - return to Normal mode without changes
    cancel_button = customtkinter.CTkButton(
        delete_button_frame, 
        text="Cancel", 
        command=lambda: show_normal_mode(app),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    cancel_button.grid(row=0, column=1, padx=5, pady=5)

    # Delete All button - remove all tasks
    delete_all_button = customtkinter.CTkButton(
        delete_button_frame, 
        text="Delete All", 
        command=lambda: confirm_delete_all_popup(app),
        fg_color="#c42b1c",  # Red color for destructive action
        hover_color="#a22315"
    )
    delete_all_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


def handle_delete_submit(app):
    """
    Process task deletion request.
    
    Shows confirmation popup before deleting.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Shows error popup if no task was selected
        - Shows confirmation popup if task was selected
    
    Returns:
        None
    """
    # Validate that a task was selected
    if app.selected_delete_var.get() == -1:
        show_popup(app, "Please select a task first")
        return
    
    # Show confirmation dialog before deleting
    confirm_delete_popup(app)


def handle_delete_confirmed(app):
    """
    Execute task deletion after confirmation.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Calls backend to delete task
        - Returns to Normal mode, refreshing the task list
    
    Returns:
        None
    """
    todo_backend.delete_task(app.selected_delete_var.get())
    show_normal_mode(app)


def confirm_delete_popup(app):
    """
    Display confirmation dialog for single task deletion.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Creates modal popup window for confirmation
    
    Returns:
        None
    """
    popup = customtkinter.CTkToplevel(app)
    popup.title("Confirm")
    popup.geometry("300x150")
    
    # Center popup relative to parent window
    center_popup(popup, app)
    
    # Make modal (blocks interaction with parent)
    popup.grab_set()

    # Confirmation message
    label = customtkinter.CTkLabel(popup, text="Delete this task?")
    label.pack(pady=20, padx=20)

    # Button container
    button_frame = customtkinter.CTkFrame(popup)
    button_frame.pack(pady=10)

    # Yes button - confirm deletion
    yes_button = customtkinter.CTkButton(
        button_frame,
        text="Yes",
        command=lambda: (handle_delete_confirmed(app), popup.destroy()),
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    yes_button.grid(row=0, column=0, padx=10)

    # No button - cancel deletion
    no_button = customtkinter.CTkButton(
        button_frame,
        text="No",
        command=popup.destroy,
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    no_button.grid(row=0, column=1, padx=10)


def confirm_delete_all_popup(app):
    """
    Display confirmation dialog for deleting all tasks.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Creates modal popup window for confirmation
    
    Returns:
        None
    """
    popup = customtkinter.CTkToplevel(app)
    popup.title("Confirm")
    popup.geometry("300x150")
    
    # Center popup relative to parent window
    center_popup(popup, app)
    
    # Make modal (blocks interaction with parent)
    popup.grab_set()

    # Warning message
    label = customtkinter.CTkLabel(
        popup, 
        text="Delete ALL tasks?", 
        text_color="red"
    )
    label.pack(pady=20, padx=20)

    # Button container
    button_frame = customtkinter.CTkFrame(popup)
    button_frame.pack(pady=10)

    # Yes button - confirm deletion of all tasks
    yes_button = customtkinter.CTkButton(
        button_frame,
        text="Yes",
        command=lambda: (handle_delete_all_confirmed(app), popup.destroy()),
        fg_color="#c42b1c",  # Red for destructive action
        hover_color="#a22315"
    )
    yes_button.grid(row=0, column=0, padx=10)

    # No button - cancel deletion
    no_button = customtkinter.CTkButton(
        button_frame,
        text="No",
        command=popup.destroy,
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    no_button.grid(row=0, column=1, padx=10)


def handle_delete_all_confirmed(app):
    """
    Execute deletion of all tasks after confirmation.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Calls backend to delete all tasks
        - Returns to Normal mode, refreshing the task list
    
    Returns:
        None
    """
    todo_backend.delete_task(app.selected_delete_var.get(), flag="All")
    show_normal_mode(app)


def show_popup(parent, message):
    """
    Display a simple error popup message with an OK button.
    
    Args:
        parent (CTk): The parent window (main app)
        message (str): Message text to display
    
    Side effects:
        - Creates modal popup window
    
    Returns:
        None
    """
    # Create new popup window
    popup = customtkinter.CTkToplevel(parent)
    popup.title("Error")
    popup.geometry("300x150")
    
    # Center popup relative to parent window
    center_popup(popup, parent)
    
    # Make modal (blocks interaction with parent)
    popup.grab_set()
    
    # Error message in red
    label = customtkinter.CTkLabel(popup, text=message, text_color="red")
    label.pack(pady=20, padx=20)
    
    # OK button to close popup
    ok_button = customtkinter.CTkButton(
        popup,
        text="OK",
        command=popup.destroy,
        fg_color=BUTTON_COLOR,
        hover_color=HOVER_COLOR
    )
    ok_button.pack(pady=10)


def center_popup(popup, parent):
    """
    Center a popup window relative to its parent window.
    
    Args:
        popup (CTkToplevel): The popup window to center
        parent (CTk): The parent window
    
    Side effects:
        - Updates popup window position
    
    Returns:
        None
    """
    # Update to get accurate dimensions
    popup.update_idletasks()
    
    # Get parent window position and size
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    
    # Get popup dimensions
    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()
    
    # Calculate center position
    x = parent_x + (parent_width - popup_width) // 2
    y = parent_y + (parent_height - popup_height) // 2
    
    # Set popup position
    popup.geometry(f"+{x}+{y}")


def show_normal_mode(app):
    """
    Return from any mode (Add/Edit/Delete/Complete) back to Normal mode.
    
    Reusable function for all mode transitions. Destroys current mode frame,
    recreates task list with fresh data, and shows action buttons.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Destroys current mode frame
        - Recreates task list with fresh data from backend
        - Shows the button frame again
    
    Returns:
        None
    
    Assumptions:
        - app.current_frame exists and contains the current mode's frame
        - app.button_frame exists and is the Normal mode button frame
    """
    # Clean up current mode interface
    app.current_frame.destroy()

    # Recreate task list with updated data from backend
    create_list(app)
    
    # Show the action buttons again
    app.button_frame.pack(pady=20)


def hide_normal_mode(app):
    """
    Hide/destroy Normal mode widgets when switching to another mode.
    
    Args:
        app (CTk): The main CTk application window
    
    Side effects:
        - Destroys scrollable frame (needs fresh data when returning)
        - Hides button frame (reused without changes)
    
    Returns:
        None
    
    Note:
        Scrollable frame destroyed because it needs fresh data when returning.
        Button frame only hidden because it's reused without changes.
    """
    app.scrollable_frame.pack_forget()
    app.scrollable_frame.destroy()
    app.button_frame.pack_forget()


if __name__ == "__main__":
    main()