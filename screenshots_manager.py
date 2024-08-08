import os
import json
import shutil
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, font
from PIL import Image, ImageTk
from natsort import natsorted


class ScreenshotsManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Screenshots Manager")
        self.master.geometry("700x880+750+350")

        # Initialize folder path and last used folder name variables
        self.folder_path = StringVar()
        self.last_folder_name = None

        self.custom_font = font.Font(size=14)

        # Listbox to display images
        self.listbox = Listbox(self.master, width=60, height=25, font=self.custom_font)
        self.listbox.pack(pady=20)

        # Buttons
        btn_edit_info = Button(self.master, text="Edit Info", command=self.edit_info)
        btn_edit_info.pack()

        btn_open_folder = Button(self.master, text="Open Folder", command=self.open_folder)
        btn_open_folder.pack()

        btn_load_info_json = Button(self.master, text="Load JSON", command=self.load_json)
        btn_load_info_json.pack()

        btn_rename_images = Button(self.master, text="Rename Images", command=self.rename_images)
        btn_rename_images.pack()

        btn_export_json = Button(self.master, text="Export JSON", command=self.export_json)
        btn_export_json.pack()

        btn_copy_images = Button(self.master, text="Copy Images", command=self.copy_images)
        btn_copy_images.pack()

        btn_load_json = Button(self.master, text="Load JSON and Delete Unlisted", command=self.load_json_and_delete)
        btn_load_json.pack()

        btn_convert_png_to_jpg = Button(self.master, text="Convert PNG to JPG", command=self.convert_png_to_jpg)
        btn_convert_png_to_jpg.pack()

        # Dictionary to store additional information
        self.image_info = {}

    def open_folder(self):
        self.folder_path.set(filedialog.askdirectory())
        self.display_images()
        self.last_folder_name = None

    def display_images(self):
        self.listbox.delete(0, END)  # Clear the listbox
        if self.folder_path.get():
            files = [file for file in os.listdir(self.folder_path.get()) if
                     file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            sorted_files = natsorted(files)  # Natural sort
            for file in sorted_files:
                file_number = os.path.splitext(file)[0]
                file_info = self.image_info.get(file_number, {})
                info_text = f"{file} - Price: {file_info.get('price', '')} - Big Note: {file_info.get('big_note', '')} - Small Note: {file_info.get('small_note', '')} - Crystal: {file_info.get('crystal', '')} - Tags: {', '.join(file_info.get('tags', []))}"
                self.listbox.insert(END, info_text)

    def rename_images(self):
        if self.folder_path.get():
            start_number = simpledialog.askinteger("Start Number", "Enter the start number:")
            if start_number is not None:
                i = start_number
                files = [file for file in os.listdir(self.folder_path.get()) if
                         os.path.splitext(file)[1].lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')]
                sorted_files = natsorted(files)  # Natural sort
                for file in sorted_files:
                    ext = os.path.splitext(file)[1]
                    new_name = f"{i:03}{ext}"
                    os.rename(os.path.join(self.folder_path.get(), file),
                              os.path.join(self.folder_path.get(), new_name))
                    i += 1
                self.display_images()

    def export_json(self):
        folder_name = self.get_folder_name()
        specific_path_json = "E:/bella-prsk.github.io/src/lib/json"  # JSON storage path
        files_dict = {}
        files = [file for file in os.listdir(self.folder_path.get()) if
                 os.path.splitext(file)[1].lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')]
        sorted_files = natsorted(files)  # Natural sort
        for file in sorted_files:
            file_number = os.path.splitext(file)[0]
            file_ext = os.path.splitext(file)[1]
            file_info = self.image_info.get(file_number, {})
            file_info["type"] = file_ext
            files_dict[file_number] = file_info

        data = {
            "folder": folder_name,
            "files": files_dict
        }
        json_filename = os.path.join(specific_path_json, f"{folder_name}_data.json")
        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON file saved to {json_filename}")

    def get_folder_name(self):
        if self.last_folder_name is None:
            self.last_folder_name = simpledialog.askstring("Folder Name", "Enter the folder name:")
        return self.last_folder_name

    def copy_images(self):
        folder_name = self.get_folder_name()
        specific_path_images = f"E:/bella-prsk.github.io/static/{folder_name}"  # Image copy path
        os.makedirs(specific_path_images, exist_ok=True)  # Ensure directory exists
        files = [file for file in os.listdir(self.folder_path.get()) if
                 os.path.splitext(file)[1].lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')]
        sorted_files = natsorted(files)  # Natural sort
        for file in sorted_files:
            shutil.copy(os.path.join(self.folder_path.get(), file), specific_path_images)
        print(f"Images copied to {specific_path_images}")

    def load_json_and_delete(self):
        json_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if json_path:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
            listed_files = {f"{key}{value['type']}" for key, value in data['files'].items()}
            existing_files = {file for file in os.listdir(self.folder_path.get()) if
                              file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))}

            files_to_delete = existing_files - listed_files
            for file in files_to_delete:
                os.remove(os.path.join(self.folder_path.get(), file))

            messagebox.showinfo("Operation Complete", f"Unlisted images deleted: {len(files_to_delete)} files.")
            self.display_images()

    def edit_info(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an image from the list.")
            return

        file_name = self.listbox.get(selected[0]).split(" - ")[0]  # Extract the file name
        file_number = os.path.splitext(file_name)[0]
        current_info = self.image_info.get(file_number, {})

        form = Toplevel(self.master)
        form.geometry("645x780+1500+300")
        form.title("Edit Image Info")

        Label(form, text="Price:").grid(row=0, column=0, padx=10, pady=5)
        price_entry = Entry(form)
        price_entry.grid(row=0, column=1, padx=10, pady=5)
        price_entry.insert(0, current_info.get('price', ''))

        Label(form, text="Crystal:").grid(row=1, column=0, padx=10, pady=5)
        crystal_entry = Entry(form)
        crystal_entry.grid(row=1, column=1, padx=10, pady=5)
        crystal_entry.insert(0, current_info.get('crystal', ''))

        Label(form, text="Big Note:").grid(row=2, column=0, padx=10, pady=5)
        big_note_entry = Entry(form)
        big_note_entry.grid(row=2, column=1, padx=10, pady=5)
        big_note_entry.insert(0, current_info.get('big_note', ''))

        Label(form, text="Small Note:").grid(row=3, column=0, padx=10, pady=5)
        small_note_entry = Entry(form)
        small_note_entry.grid(row=3, column=1, padx=10, pady=5)
        small_note_entry.insert(0, current_info.get('small_note', ''))

        Label(form, text="Tags:").grid(row=4, column=0, padx=10, pady=5, columnspan=4)

        # Load tags from the JSON file
        with open("tag_colors.json", 'r') as tag_file:
            self.tag_colors = json.load(tag_file)

        # Display checkboxes for tags in 6 rows and 4 columns
        tag_vars = {}
        row = 5
        col = 0
        max_cols = 4
        for tag, color in self.tag_colors.items():
            var = BooleanVar()
            if 'tags' in current_info and tag in current_info['tags']:
                var.set(True)
            Checkbutton(form, text=tag, variable=var).grid(row=row, column=col, padx=10, pady=2, sticky=W)
            tag_vars[tag] = var
            col += 1
            if col >= max_cols:
                col = 0
                row += 1


        # Load and display the image
        img_path = os.path.join(self.folder_path.get(), file_name)
        img = Image.open(img_path)
        img = img.resize((640, 360))  # Resize the image to fit the form
        img = ImageTk.PhotoImage(img)
        img_label = Label(form, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.grid(row=row + 2, column=0, columnspan=4, pady=10)

        def save_info():
            tags = [tag for tag, var in tag_vars.items() if var.get()]
            self.image_info[file_number] = {
                "price": price_entry.get(),
                "crystal": crystal_entry.get(),
                "big_note": big_note_entry.get(),
                "small_note": small_note_entry.get(),
                "tags": tags
            }
            form.destroy()
            print(f"Information updated for {file_name}")
            self.display_images()
            self.export_json()

        Button(form, text="Save", command=save_info).grid(row=row + 1, columnspan=4, pady=10)


    def load_json(self):
        json_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if json_path:
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)

            self.last_folder_name = data.get('folder', None)
            self.image_info = {file_number: info for file_number, info in data['files'].items()}
            self.display_images()

    def convert_png_to_jpg(self):
        jpg_folder_path = os.path.join(self.folder_path.get(), 'jpg')
        if not os.path.exists(jpg_folder_path):
            os.makedirs(jpg_folder_path)

        for filename in os.listdir(self.folder_path.get()):
            if filename.endswith(".png"):
                file_path = os.path.join(self.folder_path.get(), filename)
                # Open the image file
                img = Image.open(file_path)
                # Define the output filename within the 'jpg' subfolder
                output_filename = os.path.join(jpg_folder_path, os.path.splitext(filename)[0] + '.jpg')
                # Convert and save the image as JPEG
                img.convert('RGB').save(output_filename, "JPEG", quality=85)

        messagebox.showinfo("Conversion Complete",
                            "All PNG files have been converted to JPEG and saved in the 'jpg' folder.")


def main():
    root = Tk()
    app = ScreenshotsManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
