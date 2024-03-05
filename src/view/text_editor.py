import tkinter as tk
from tkinter import filedialog

from src.controller import Controller


class TextEditor:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.root = tk.Tk()

        # Create a text widget for line numbers
        self.line_number_bar = tk.Text(self.root, width=4, state='disabled', bg='lightgrey', padx=5)
        self.line_number_bar.grid(row=0, column=0, sticky='nsew')

        # Create a text widget
        self.text = tk.Text(self.root)
        self.text.grid(row=0, column=1, sticky='nsew')
        default_text = '(*header*)\n%%\n(*rules*)\n%%\n(*trailer*)'
        self.text.insert(tk.INSERT, default_text)

        # Create a disabled text widget to display program output
        self.console = tk.Text(self.root, state='disabled', height=10, bg='darkgrey')
        self.console.grid(row=1, column=0, columnspan=2, sticky='nsew')

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

        self.bind_update_line_numbers()

        self.root.bind_all('<Control-s>', self.save_file)  # Ctrl + S to save a file
        self.root.bind_all('<Control-o>', self.open_file)  # Ctrl + O to open a file
        self.root.bind_all('<Control-r>', self.run_file)  # Ctrl + R to run the program
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.current_file = None  # To keep track of the current file

        # Synchronize scrolling
        self.text.config(yscrollcommand=self.scroll_line_numbers)
        self.line_number_bar.config(yscrollcommand=self.scroll_text)

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
                    defaultextension=".lex",
                    filetypes=[("LEX files", "*.lex"), ("All files", "*.*")]
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
        self.console.see(tk.END)
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

    def update_line_numbers(self, event=None):
        # Delete the current content of the line number bar
        self.line_number_bar.config(state='normal')
        self.line_number_bar.delete('1.0', tk.END)

        # Insert the new line numbers
        num_of_lines = self.text.index('end-1c').split('.')[0]
        line_numbers_string = "\n".join(str(no) for no in range(1, int(num_of_lines) + 1))
        self.line_number_bar.insert('1.0', line_numbers_string)

        self.line_number_bar.config(state='disabled')

    def update_line_numbers_on_change(self, event=None):
        self.update_line_numbers()
        self.scroll_line_numbers('moveto', '1.0')

    def bind_update_line_numbers(self):
        self.text.bind('<Key>', self.update_line_numbers_on_change)
        self.text.bind('<Button-1>', self.update_line_numbers_on_change)
        self.text.bind('<<Change>>', self.update_line_numbers_on_change)
        self.text.bind('<<Modified>>', self.update_line_numbers_on_change)

    def scroll_line_numbers(self, *args):
        try:
            self.line_number_bar.yview(*args)
        except tk.TclError:
            # Handle the case when the scroll command argument is a float
            pass

    def scroll_text(self, *args):
        try:
            self.text.yview(*args)
        except tk.TclError:
            # Handle the case when the scroll command argument is a float
            pass
