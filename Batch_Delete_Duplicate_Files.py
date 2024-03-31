import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

def get_file_hash(file_path):
    # Calculate the hash of the file content
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(folder_path, extensions):
    # Dictionary to store file hashes and corresponding file paths
    hash_dict = {}
    # List to store duplicate files
    duplicate_files = []

    # Iterate through all files in the specified folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in extensions):
            file_hash = get_file_hash(file_path)
            if file_hash in hash_dict:
                # Duplicate found
                duplicate_files.append((file_path, hash_dict[file_hash]))
            else:
                # Add hash and file path to the dictionary
                hash_dict[file_hash] = file_path

    return duplicate_files

def delete_selected_file():
    selected_idx = listbox.curselection()
    if selected_idx:
        selected_idx = int(selected_idx[0])
        duplicate_path, _ = duplicate_files[selected_idx]
        os.remove(duplicate_path)
        messagebox.showinfo("File Deleted", "File deleted successfully.")
        update_listbox()
    else:
        messagebox.showwarning("No Selection", "Please select a file to delete.")

def delete_all_duplicate_files():
    for duplicate_path, _ in duplicate_files:
        os.remove(duplicate_path)
    messagebox.showinfo("All Duplicate Files Deleted", "All duplicate files deleted successfully.")
    update_listbox()

def close_program():
    window.destroy()

def update_listbox():
    listbox.delete(0, tk.END)
    for idx, (duplicate_path, original_path) in enumerate(duplicate_files):
        _, file_name = os.path.split(duplicate_path)
        listbox.insert(tk.END, f"{idx + 1}: {file_name}")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_path)
        global duplicate_files
        duplicate_files = find_duplicate_files(folder_path, extensions)
        update_listbox()

# Create the main window
window = tk.Tk()
window.title("Duplicate File Finder")

# Create and place widgets
label_folder = tk.Label(window, text="Folder Path:")
label_folder.pack()

entry_folder = tk.Entry(window, width=50)
entry_folder.pack()

button_browse = tk.Button(window, text="Browse", command=browse_folder)
button_browse.pack()

listbox = tk.Listbox(window, height=10, width=80)
listbox.pack()

button_delete = tk.Button(window, text="Delete Selected File", command=delete_selected_file)
button_delete.pack()

button_delete_all = tk.Button(window, text="Delete All Duplicate Files", command=delete_all_duplicate_files)
button_delete_all.pack()

button_close = tk.Button(window, text="Close Program", command=close_program)
button_close.pack()

# Initialize the duplicate files list
duplicate_files = []

# Specify the file extensions to search for duplicates
extensions = ['.pdf', '.docx']

# Run the main loop
window.mainloop()
