import tkinter as tk
from tkinter import filedialog

from src.controller import Controller


class TextEditor:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.root = tk.Tk()
        # Create a text widget
        self.text = tk.Text(self.root)
        self.text.grid(row=0, sticky='nsew')

        # Create a disabled text widget to display program output
        self.console = tk.Text(self.root, state='disabled', height=10)
        self.console.grid(row=1, sticky='nsew')

        # Add a file menu to the menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        # File Option
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open...", command=self.open_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        # Run Option
        self.menu.add_command(label="Run", command=self.run_file)

        self.root.bind_all('<Control-s>', self.save_file)  # Ctrl + S to save a file
        self.root.bind_all('<Control-o>', self.open_file)  # Ctrl + O to open a file
        self.root.bind_all('<Control-r>', self.run_file)  # Ctrl + R to run the program
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.current_file = None  # To keep track of the current file

    def new_file(self):
        self.text.delete(1.0, tk.END)

    def open_file(self, event=None):
        try:
            file_path = filedialog.askopenfilename()
            with open(file_path, 'r') as file:
                content = file.read()
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.INSERT, content)
            self.current_file = file_path
        except FileNotFoundError:
            pass

    def save_file(self, event=None):
        try:
            if self.current_file:
                # If a file is currently open, save to this file
                with open(self.current_file, 'w') as file:
                    content = self.text.get(1.0, tk.END)
                    file.write(content)
            else:
                # If no file is currently open, open the save file dialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".yal",
                    filetypes=[("YAL files", "*.yal"), ("All files", "*.*")]
                )
                with open(file_path, 'w') as file:
                    content = self.text.get(1.0, tk.END)
                    file.write(content)

                self.current_file = file_path
        except FileNotFoundError:
            pass

    def run_file(self, event=None):
        try:
            content = self.text.get(1.0, tk.END)
            self.print_console("Running file...")

            self.controller.run_file(self.print_console, content)
        except Exception as e:
            self.print_console(f"Error: {e}")

    def print_console(self, message):
        self.console.config(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.config(state='disabled')

    def run(self):
        self.root.mainloop()

    def on_close(self):
        """
        This method is called when the user closes the application window.
        """
        # Save the current file
        self.save_file()

        # Destroy the tkinter root window
        self.root.destroy()
