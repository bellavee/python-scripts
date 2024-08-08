import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os


def convert_png_to_jpg(folder_path):
    # Create a new subfolder 'jpg' within the selected folder to store the JPEG files
    jpg_folder_path = os.path.join(folder_path, 'jpg')
    if not os.path.exists(jpg_folder_path):
        os.makedirs(jpg_folder_path)

    # Iterate through all the files in the selected folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            # Open the image file
            img = Image.open(file_path)
            # Define the output filename within the 'jpg' subfolder
            output_filename = os.path.join(jpg_folder_path, os.path.splitext(filename)[0] + '.jpg')
            # Convert and save the image as JPEG
            img.convert('RGB').save(output_filename, "JPEG", quality=85)

    messagebox.showinfo("Conversion Complete",
                        "All PNG files have been converted to JPEG and saved in the 'jpg' folder.")


def browse_folder():
    # Let the user select a folder
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # Process all PNG files in the folder
        convert_png_to_jpg(folder_selected)


def create_app():
    root = tk.Tk()
    root.title("PNG to JPEG Converter")
    root.geometry("300x300+3200+0")

    # Create a button to browse for the folder
    browse_button = tk.Button(root, text="Browse Folder", command=browse_folder)
    browse_button.pack(pady=20)

    # Run the application
    root.mainloop()


if __name__ == "__main__":
    create_app()
