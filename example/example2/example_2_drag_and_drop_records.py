import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag & Drop File Selector")

        # Enable native drag-and-drop capability
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_files)

        # Create a drop zone
        self.drop_frame = tk.Label(root, text="Drag and drop files here", bg="lightgray", width=50, height=10)
        self.drop_frame.pack(pady=10)

        # Create a listbox to display selected files
        self.file_listbox = tk.Listbox(root, width=60, height=10)
        self.file_listbox.pack(pady=10)

        # Buttons for manual selection and finalizing selection
        self.select_button = tk.Button(root, text="Select Files", command=self.open_file_dialog)
        self.select_button.pack(pady=5)

        self.done_button = tk.Button(root, text="Done", command=self.finish_selection)
        self.done_button.pack(pady=5)

        # Store selected file paths
        self.selected_files = []

    def open_file_dialog(self):
        """Opens a file dialog to manually select files."""
        file_paths = self.root.tk.splitlist(tk.filedialog.askopenfilenames(title="Select files"))
        if file_paths:
            self.selected_files.extend(file_paths)
            self.update_file_list()

    def drop_files(self, event):
        """Handles dropped files into the window."""
        file_paths = self.root.tk.splitlist(event.data)
        if file_paths:
            self.selected_files.extend(file_paths)
            self.update_file_list()

    def update_file_list(self):
        """Updates the listbox with selected filenames."""
        self.file_listbox.delete(0, tk.END) # Clear listbox
        for file in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file)) # Show filenames only

    def finish_selection(self):
        """Closes the window and returns selected files."""
        self.root.quit() # Close the window

def launch():
    """Starts the GUI and returns selected files."""
    root = TkinterDnD.Tk()
    app = DragDropApp(root)
    root.mainloop() # Runs the Tkinter event loop
    return app.selected_files # Returns selected files after the window closes

# Example usage:
files = launch()
print("Selected files:", files)