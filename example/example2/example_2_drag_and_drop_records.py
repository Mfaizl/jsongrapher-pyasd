import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import JSONGrapherRC

global_records_list = []

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSONGrapher")

        # Enable native drag-and-drop capability
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.drop_files)

        # Create a drop zone
        self.drop_frame = tk.Label(root, text="Drag and drop files here \n\n Click End When Finished", bg="lightgray", width=50, height=10)
        self.drop_frame.pack(pady=10)

        # Create a listbox to display selected files
        self.file_listbox = tk.Listbox(root, width=60, height=10)
        self.file_listbox.pack(pady=10)

        # Buttons for manual selection and finalizing selection
        self.select_button = tk.Button(root, text="Select Files By Browsing", command=self.open_file_dialog)
        self.select_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear Files List", command=self.clear_file_list)  # New "Clear" button
        self.clear_button.pack(pady=5)

        self.done_button = tk.Button(root, text="End", command=self.finish_selection)
        self.done_button.pack(pady=5)

        # Store selected file paths
        self.selected_files = []

    def clear_file_list(self):
        """Clears the listbox and resets selected files."""
        self.file_listbox.delete(0, tk.END)  # Clear listbox
        self.selected_files = []  # Reset file list
        print("File list cleared!")  # Optional debug message

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
        for filename_and_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(filename_and_path)) # Show filenames only
        print("line 55", filename_and_path)
        if len(global_records_list) == 0:
            first_record = JSONGrapherRC.create_new_JSONGrapherRecord()
            first_record.import_from_file(filename_and_path)
            #index 0 will be the one we merge into.
            global_records_list.append(first_record)
            #index 1 will be where we store the first record, so we append again.
            global_records_list.append(first_record)
        else:
            current_record = JSONGrapherRC.create_new_JSONGrapherRecord()
            current_record.import_from_file(filename_and_path)
            global_records_list.append(current_record)
            #now create merged record.
            global_records_list[0] = JSONGrapherRC.merge_JSONGrapherRecords([global_records_list[0], current_record])
        #plot the index 0, which is the most up to date merged record.
        global_records_list[0].plot_with_plotly()

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