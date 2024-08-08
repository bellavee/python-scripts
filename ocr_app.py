import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, StringVar, OptionMenu, Label
import os
from PIL import Image
import pytesseract
import json

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Image to Text Converter")

        self.config_file = "config.json"
        self.image_dir = ""
        self.output_dir = "output_texts"
        os.makedirs(self.output_dir, exist_ok=True)

        self.languages = {
            "English": "eng",
            "Simplified Chinese": "chi_sim",
            "Traditional Chinese": "chi_tra",
            # Add more languages here as needed
        }
        self.selected_language = StringVar(value="English")

        self.setup_ui()
        self.load_last_directory()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        self.select_folder_button = tk.Button(frame, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=5)

        self.language_menu = OptionMenu(frame, self.selected_language, *self.languages.keys())
        self.language_menu.pack(pady=5)

        self.image_listbox = Listbox(frame, selectmode=tk.SINGLE, width=50)
        self.image_listbox.pack(pady=5)

        self.export_all_button = tk.Button(frame, text="Export All Images to Text", command=self.export_all_images)
        self.export_all_button.pack(pady=5)

        self.export_selected_button = tk.Button(frame, text="Export Selected Image to Text", command=self.export_selected_image)
        self.export_selected_button.pack(pady=5)

        self.path_label = Label(frame, text="No folder selected")
        self.path_label.pack(pady=5)

    def select_folder(self):
        self.image_dir = filedialog.askdirectory()
        if self.image_dir:
            self.list_images()
            self.save_last_directory()
            self.update_path_label()

    def list_images(self):
        self.image_listbox.delete(0, tk.END)
        for filename in os.listdir(self.image_dir):
            if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                self.image_listbox.insert(tk.END, filename)

    def export_all_images(self):
        for filename in os.listdir(self.image_dir):
            if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                self.perform_ocr(filename)

        messagebox.showinfo("Success", "All images have been exported to text.")

    def export_selected_image(self):
        selected = self.image_listbox.curselection()
        if selected:
            filename = self.image_listbox.get(selected[0])
            self.perform_ocr(filename)
            messagebox.showinfo("Success", f"{filename} has been exported to text.")
        else:
            messagebox.showwarning("Warning", "No image selected.")

    def perform_ocr(self, filename):
        image_path = os.path.join(self.image_dir, filename)
        image = Image.open(image_path)

        language_code = self.languages[self.selected_language.get()]
        text = pytesseract.image_to_string(image, lang=language_code)

        lines = text.splitlines()
        processed_text = ""
        for line in lines:
            if line.strip():
                if processed_text and not processed_text.endswith('\n\n'):
                    processed_text += " "
                processed_text += line.strip()
            else:
                if not processed_text.endswith('\n\n'):
                    processed_text += "\n\n"

        output_filename = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(self.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)

        print(f"Processed {filename} and saved to {output_path}")

    def save_last_directory(self):
        with open(self.config_file, 'w') as f:
            json.dump({"last_directory": self.image_dir}, f)

    def load_last_directory(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.image_dir = config.get("last_directory", "")
                if self.image_dir:
                    self.list_images()
                    self.update_path_label()

    def update_path_label(self):
        self.path_label.config(text=f"Current folder: {self.image_dir}")

if __name__ == "__main__":
    # Path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your installation

    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
