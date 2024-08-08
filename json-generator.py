import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json


def generate_json_for_folder(folder_path):
    # Extract the folder name
    folder_name = os.path.basename(folder_path)
    files_dict = {}

    # Iterate through all the files in the selected folder
    for filename in os.listdir(folder_path):
        name, ext = os.path.splitext(filename)
        if ext.lower() in ['.png', '.jpg', '.jpeg']:  # Filter for image files
            files_dict[name] = ext

    # Create a dictionary to store the folder and files
    folder_files_json = {
        "folder": folder_name,
        "files": files_dict
    }

    # Convert the dictionary to JSON format
    json_output = json.dumps(folder_files_json, indent=4)

    # Get the parent directory of the selected folder
    parent_directory = os.path.dirname(folder_path)

    # Create the JSON filename in the parent directory
    json_filename = os.path.join(parent_directory, f"{folder_name}_data.json")

    # Write the JSON to a file in the parent directory
    with open(json_filename, 'w') as json_file:
        json_file.write(json_output)

    messagebox.showinfo("JSON Generated", f"JSON has been generated and saved as {json_filename}")


def browse_folder():
    # Let the user select a folder
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # Generate JSON for the selected folder
        generate_json_for_folder(folder_selected)


def create_app():
    root = tk.Tk()
    root.title("Folder to JSON Converter")
    root.geometry("300x300+3200+0")

    # Create a button to browse for the folder
    browse_button = tk.Button(root, text="Browse Folder and Generate JSON", command=browse_folder)
    browse_button.pack(pady=20)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    create_app()
