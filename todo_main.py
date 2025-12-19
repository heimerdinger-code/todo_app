"""
Main entry point for the To-Do List Application.

This module serves as the application launcher. It imports and runs
the frontend GUI while ensuring proper error handling for dependencies.
"""

import sys

def main():
    """
    Application entry point with dependency checking.
    
    Attempts to import and run the frontend. Provides helpful error
    messages if dependencies are missing.
    
    Returns:
        None
    
    Exits:
        Exits with code 1 if dependencies are missing
    """
    try:
        import customtkinter
    except ImportError:
        print("Error: CustomTkinter is not installed.")
        print("Please install it using: pip install customtkinter")
        sys.exit(1)
    
    try:
        import todo_frontend
    except ImportError:
        print("Error: todo_frontend.py not found.")
        print("Make sure todo_frontend.py is in the same directory.")
        sys.exit(1)
    
    try:
        import todo_backend
    except ImportError:
        print("Error: todo_backend.py not found.")
        print("Make sure todo_backend.py is in the same directory.")
        sys.exit(1)
    
    # Run the application
    print("Starting To-Do List Application...")
    todo_frontend.main()


if __name__ == "__main__":
    main()