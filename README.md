# 📝 To-Do List Application

A modern, user-friendly desktop to-do list application built with Python and CustomTkinter. Features a clean GUI with full CRUD (Create, Read, Update, Delete) functionality and persistent storage.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Add Tasks**: Create new tasks with optional descriptions
- **Edit Tasks**: Modify existing task names and descriptions
- **Complete Tasks**: Mark tasks as done with visual checkmarks
- **Delete Tasks**: Remove individual tasks or clear all at once
- **Persistent Storage**: All tasks saved to CSV file
- **Modern UI**: Clean interface built with CustomTkinter
- **Input Validation**: Error handling with helpful popup messages

## 📸 Screenshots

*(Add screenshots of your application here)*

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/todo-list-app.git
   cd todo-list-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
todo-list-app/
│
├── main.py              # Application entry point
├── todo_frontend.py     # GUI interface and user interactions
├── todo_backend.py      # Data management and CSV operations
├── tasks.csv           # Task storage (auto-generated)
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
└── LICENSE            # Project license
```

## 💻 Usage

### Adding a Task
1. Click the **Add** button
2. Enter a task name (required)
3. Optionally add a description
4. Click **Add** to save or **Cancel** to discard

### Editing a Task
1. Click the **Edit** button
2. Select a task from the list
3. Click **Next**
4. Modify the task name or description
5. Click **Edit** to save changes

### Completing a Task
1. Click the **Complete** button
2. Select an incomplete task
3. Click **Complete** to mark it as done

### Deleting Tasks
1. Click the **Delete** button
2. Select a task to remove
3. Click **Delete** for single task or **Delete All** for all tasks
4. Confirm your choice in the popup

## 🛠️ Technical Details

### Technologies Used
- **Python 3.7+**: Core programming language
- **CustomTkinter**: Modern GUI framework
- **CSV**: Data persistence

### Key Components

**todo_backend.py**
- Handles CRUD operations
- Manages CSV file I/O
- Maintains in-memory task list

**todo_frontend.py**
- Creates and manages GUI
- Handles user interactions
- Implements modal dialogs

**main.py**
- Application launcher
- Dependency validation
- Error handling

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@heimerdinger-code](https://github.com/heimerdinger-code)
- Email: get.jinxed.qwerty@gmail.com

## 🙏 Acknowledgments

- CustomTkinter for the modern GUI framework
- AI for excellent documentation


---

⭐ If you found this project helpful, please consider giving it a star!
