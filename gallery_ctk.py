import customtkinter as ctk
from tkinter import filedialog, Menu, Canvas, Label, Scrollbar, Entry, Frame, messagebox, simpledialog, StringVar, PhotoImage
from PIL import Image, ImageGrab
import os
import json
import re
import io
import subprocess
from screeninfo import get_monitors

class PhotoGalleryApp(ctk.CTk):
    def __init__(self, master=None):
        super().__init__(master)
        ctk.set_appearance_mode("Dark")

        self.notes = {}
        self.tag_colors = {}

        self.load_tag_data()

        self.available_tags = list(self.tag_colors.keys())
        self.tag_widgets = {}

        # Prompt for background and text colors using ctk entry dialogs
        self.bg_color = '#303030'
        self.text_color = '#ffffff'

        self.title("Photo Gallery")
        self.geometry('1080x1200+800+100')

        self.monitor_width = None

        self.configure(bg=self.bg_color)

        self.button_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.button_frame.pack(pady=10, padx=20)

        # Buttons setup for each action, packed horizontally in the frame
        self.load_images_button = ctk.CTkButton(self.button_frame, text="Load Images", command=self.load_images)
        self.load_images_button.pack(side="left", padx=10, fill='x', expand=True)

        self.refresh_button = ctk.CTkButton(self.button_frame, text="Refresh", command=self.refresh_images)
        self.refresh_button.pack(side="left", padx=10, fill='x', expand=True)

        self.save_data_button = ctk.CTkButton(self.button_frame, text="Save Data", command=self.save_data)
        self.save_data_button.pack(side="left", padx=10, fill='x', expand=True)

        self.load_data_button = ctk.CTkButton(self.button_frame, text="Load Data", command=self.load_data)
        self.load_data_button.pack(side="left", padx=10, fill='x', expand=True)

        self.rename_images_button = ctk.CTkButton(self.button_frame, text="Rename Images", command=self.rename_images)
        self.rename_images_button.pack(side="left", padx=10, fill='x', expand=True)

        self.settings_button = ctk.CTkButton(self.button_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side="left", padx=10, fill='x', expand=True)

        self.settings_dialog = None
        self.settings_open = False

        # Create a dropdown menu to select the number of columns
        self.column_var = StringVar(value="3")
        self.column_dropdown = ctk.CTkOptionMenu(self.button_frame, variable=self.column_var, values=["1", "2", "3", "4", "5"], command=self.refresh_images)
        self.column_dropdown.pack(side="left", padx=10, fill='x', expand=True)

        self.manage_tags_button = ctk.CTkButton(self.button_frame, text="Manage Tags", command=self.manage_tags)
        self.manage_tags_button.pack(side="left", padx=10)

        self.show_tags_system = True  # State to control visibility of the add tag system
        self.tag_system_switch = ctk.CTkSwitch(self.button_frame, text="Show Tag System",
                                               command=self.toggle_tag_system)
        self.tag_system_switch.pack(side="left", padx=10)
        self.tag_system_switch.select()

        # Editable title setup using customtkinter CTkEntry
        self.title_var = StringVar(value="Gallery")
        self.title_entry = ctk.CTkEntry(self, textvariable=self.title_var, placeholder_text="Gallery", height=50, font=('Segoe UI', 40, 'bold'), justify='center',
                                        fg_color=self.bg_color, border_color=self.bg_color, text_color=self.text_color)
        self.title_entry.pack(side="top", fill="x", padx=20, pady=10)

        # Setup a scrollable frame using Canvas and Scrollbar from tkinter as customtkinter doesn't provide these
        self.canvas = ctk.CTkCanvas(self, bg='#242424', highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, command=self.canvas.yview, orientation='vertical')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color='#242424')
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.image_folder = ''
        self.settings()


    def is_valid_hex_color(self, color):
        # This function checks if the input string is a valid hex color
        if re.match(r"^#[A-Fa-f0-9]{6}$", color):
            return True
        else:
            return False


    def load_images(self):
        self.image_folder = filedialog.askdirectory(title="Select Folder with Images")
        if not self.image_folder:
            return
        self.display_images(self.image_folder)


    def refresh_images(self, *_):
        if self.image_folder:
            self.display_images(self.image_folder)


    def update_notes(self, filename, note):
        """Update the note for the given filename."""
        self.notes[filename] = note


    def settings(self):
        self.settings_dialog = ctk.CTkToplevel(self)
        self.settings_dialog.title("Select Monitor and Color Settings")
        self.settings_dialog.geometry('400x400+1050+500')
        self.settings_open = True

        # Setup the monitor selection
        frame = ctk.CTkFrame(self.settings_dialog)
        frame.pack(expand=True, padx=20, pady=20)

        monitor_label = ctk.CTkLabel(frame, text="Select a Monitor:")
        monitor_label.pack(anchor='w', padx=20, pady=10)

        monitors = get_monitors()
        monitor_var = StringVar(value=monitors[0].width)  # Default to the first monitor's width

        for monitor in monitors:
            radio = ctk.CTkRadioButton(frame, text=f"{monitor.width}x{monitor.height}",
                                       variable=monitor_var, value=str(monitor.width))
            radio.pack(anchor='w', padx=10, pady=2)

        # Color selection for background
        bg_color_label = ctk.CTkLabel(frame, text="Enter Background Color (hex):")
        bg_color_label.pack(anchor='w', padx=20, pady=(10, 2))
        bg_color_entry = ctk.CTkEntry(frame)
        bg_color_entry.insert(0, self.bg_color)
        bg_color_entry.pack(fill='x', padx=20, pady=(0, 10))

        def confirm():
            new_bg_color = bg_color_entry.get()
            new_monitor_width = int(monitor_var.get())
            changes_applied = False

            if self.is_valid_hex_color(new_bg_color) and new_bg_color != self.bg_color:
                self.bg_color = new_bg_color
                self.text_color = self.set_text_color(new_bg_color)
                changes_applied = True
            if new_monitor_width != self.monitor_width:
                self.monitor_width = new_monitor_width
                changes_applied = True

            if changes_applied:
                self.apply_settings()

            self.settings_open = False
            self.settings_dialog.destroy()

        confirm_button = ctk.CTkButton(frame, text="Confirm", command=confirm)
        confirm_button.pack(pady=20)

        manage_tags_button = ctk.CTkButton(frame, text="Manage Tags", command=self.manage_tags)
        manage_tags_button.pack(pady=(0, 20))

        self.settings_dialog.transient(self)  # Make the self.settings_dialog modal
        self.settings_dialog.wait_window()


    def apply_settings(self):
        # Apply color settings across UI components
        self.configure(bg=self.bg_color)
        self.title_entry.configure(fg_color=self.bg_color, text_color=self.text_color)

        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.bg_color)
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, ctk.CTkLabel):
                        subwidget.configure(text_color=self.text_color)

        # Recalculate and update UI layout for new monitor width
        if self.image_folder:
            self.display_images(self.image_folder)


    def open_settings(self):
        if hasattr(self, 'settings_open') and self.settings_open:
            # Try to bring the settings window to the front if it's already open
            try:
                self.settings_dialog.lift()
            except:
                # If the dialog is closed or deleted, open a new one
                self.settings_open = False
                self.settings()
        else:
            self.settings()


    def is_dark(self, color):
        """Determine if the color is dark or light based on its luminance."""
        r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))  # Extract RGB from hex
        luminance = 0.299 * r + 0.587 * g + 0.114 * b  # Luminance calculation
        return luminance < 145  # Return True if dark, False if light


    def set_text_color(self, bg_color):
        if self.is_dark(bg_color):
            return '#ffffff'
        return '#242424'


    def manage_tags(self):
        # Create a new top-level window
        tag_window = ctk.CTkToplevel(self)
        tag_window.title("Manage Tags")
        tag_window.geometry('400x400+850+300')

        # Frame for listing existing tags
        list_frame = ctk.CTkScrollableFrame(tag_window, fg_color=self.bg_color)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Function to refresh the list of tags
        def refresh_tag_list():
            for widget in list_frame.winfo_children():
                widget.destroy()
            for tag, color in self.tag_colors.items():
                text_color = self.set_text_color(color)
                tag_label_frame = ctk.CTkFrame(list_frame, fg_color=self.bg_color)
                tag_label_frame.pack(fill='x', pady=2)

                tag_label = ctk.CTkLabel(tag_label_frame, text=f"{tag}: {color}", fg_color=color, text_color=text_color)
                tag_label.pack(side='left', fill='x', expand=True)

                delete_button = ctk.CTkButton(tag_label_frame, text='Delete', command=lambda t=tag: delete_tag(t))
                delete_button.pack(side='right', padx=10)

        # Function to delete a tag
        def delete_tag(tag):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the tag '{tag}'?"):
                del self.tag_colors[tag]
                self.save_tag_data()  # Save after deletion
                refresh_tag_list()

        refresh_tag_list()  # Initial population of the list

        # Frame for adding a new tag
        add_frame = ctk.CTkFrame(tag_window)
        add_frame.pack(fill='x', padx=20, pady=20)

        # Entry for the new tag name
        tag_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter new tag name")
        tag_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # Entry for the new tag color
        color_entry = ctk.CTkEntry(add_frame, placeholder_text="Enter color (hex)")
        color_entry.pack(side='left', fill='x', expand=True)
        color_entry.insert(0, '#')

        # Function to add a new tag
        def add_tag():
            tag = tag_entry.get()
            color = color_entry.get()
            if tag and color:
                if self.is_valid_hex_color(color):
                    self.tag_colors[tag] = color
                    self.save_tag_data()  # Save after adding a new tag
                    refresh_tag_list()
                    tag_entry.delete(0, 'end')
                    color_entry.delete(0, 'end')
                    color_entry.insert(0, '#')
                else:
                    messagebox.showerror("Error", "Color must be a valid hex code (e.g., #FF0000).")

        # Button to add the new tag
        add_button = ctk.CTkButton(add_frame, text="Add Tag", command=add_tag)
        add_button.pack(padx=(10, 0))

        # Ensure the window is modal
        tag_window.transient(self)
        tag_window.grab_set()
        self.wait_window(tag_window)


    def display_images(self, folder, notes=None):
        tags = notes or {}
        image_paths = [os.path.join(folder, f) for f in os.listdir(folder) if
                       f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        folder_name = os.path.basename(folder)
        file_data = {'folder': folder_name, 'files': {}}
        for path in image_paths:
            filename = os.path.splitext(os.path.basename(path))[0]
            extension = os.path.splitext(path)[1]
            file_data['files'][filename] = extension

        self.export_json(file_data, folder)

        # Create a list of (path, number of tags) tuples
        tagged_images = [(path, len(tags.get(os.path.splitext(os.path.basename(path))[0], []))) for path in image_paths]

        # Sort images by the number of tags, descending
        tagged_images.sort(key=lambda x: x[1], reverse=True)

        # Proceed with displaying images
        col_count = 0
        row_count = 0
        columns = int(self.column_var.get())
        available_width = self.monitor_width - 20 * (columns + 1)
        image_width = available_width // columns
        image_height = int(image_width * 9 / 16)
        base_padding = 8
        size = image_width, image_height

        for (path, tag_count) in tagged_images:
            filename = os.path.splitext(os.path.basename(path))[0]
            img = Image.open(path)
            img.thumbnail(size)
            padx = (20, base_padding) if col_count == 0 else (
            base_padding, 20) if col_count == columns - 1 else base_padding

            ct_image = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            image_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=0, fg_color=self.bg_color)
            image_frame.grid(row=row_count, column=col_count, padx=padx, pady=base_padding)

            image_label = ctk.CTkLabel(image_frame, image=ct_image, text='')
            image_label.image = ct_image
            image_label.pack()

            text_label = ctk.CTkLabel(image_frame, text=filename, font=('Segoe UI', 24, 'bold'),
                                      text_color=self.text_color)
            text_label.pack(pady=5)
            text_label.bind("<Button-1>",
                            lambda event, path=path, label=text_label: self.edit_filename(event, path, label))

            current_tags = tags.get(filename, [])
            tag_widget = self.create_tag_widget(image_frame, filename, current_tags)
            if self.show_tags_system:
                tag_widget.pack(pady=5)
            else:
                tag_widget.pack_forget()

            col_count += 1
            if col_count >= columns:
                col_count = 0
                row_count += 1

        self.update_scroll_region()

    def update_scroll_region(self):
        self.canvas.update_idletasks()  # Ensure the canvas is updated
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def toggle_tag_system(self):
        self.show_tags_system = not self.show_tags_system
        for frame, widgets in self.tag_widgets.items():
            tag_combobox = widgets['combobox']
            add_tag_button = widgets['add_button']
            if tag_combobox.winfo_exists() and add_tag_button.winfo_exists():
                if self.show_tags_system:
                    tag_combobox.pack(side='left', padx=5)
                    add_tag_button.pack(side='right', padx=5)
                else:
                    tag_combobox.pack_forget()
                    add_tag_button.pack_forget()

    def create_tag_widget(self, parent, filename, tags=[]):
        tag_frame = ctk.CTkFrame(parent, corner_radius=5, fg_color=self.bg_color)
        tag_frame.pack(side='left', expand=True, padx=10, pady=(0, 5))

        # Function to get tag color from the dictionary
        def get_tag_color(tag):
            return self.tag_colors.get(tag, '#FFFFFF')  # Default color

        def get_current_tag():
            for tag in tags:
                color = get_tag_color(tag)
                text_color = self.set_text_color(color)
                tag_button = ctk.CTkButton(tag_frame, text=tag, width=50, height=25,
                                           fg_color=color, text_color=text_color,
                                           corner_radius=5, command=lambda t=tag: remove_tag(t))
                tag_button.pack(side='left', fill='both', expand=True, padx=5, pady=(0, 5))

        # Display current tags as buttons
        get_current_tag()

        # Add tag ComboBox

        tag_combobox = ctk.CTkComboBox(tag_frame, values=self.available_tags, width=100, height=25)
        add_tag_button = ctk.CTkButton(tag_frame, text='Add', width=50, height=25,
                                       command=lambda: add_tag_from_combobox())
        add_tag_button.pack(side='right', padx=5, pady=(0, 5))
        tag_combobox.pack(side='right', padx=5, pady=(0, 5))

        # Add references to the dictionary using frame identifier
        self.tag_widgets[tag_frame] = {
            'combobox': tag_combobox,
            'add_button': add_tag_button
        }

        def add_tag_from_combobox():
            new_tag = tag_combobox.get()
            if new_tag and new_tag not in tags:
                tags.append(new_tag)
                self.update_tags(filename, tags)
                refresh_tag_display()
                tag_combobox.set('')

        def remove_tag(tag):
            if tag in tags:
                tags.remove(tag)
                self.update_tags(filename, tags)
                refresh_tag_display()

        def refresh_tag_display():
            # Clear current tags and re-display them
            for widget in tag_frame.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget('text') != 'Add':
                    widget.destroy()
            get_current_tag()

        return tag_frame

    def update_tags(self, filename, tags):
        self.notes[filename] = tags

    def edit_filename(self, event, path, label):
        # Retrieve the current text using .cget()
        original_filename = label.cget("text")

        # Create an entry and set the initial text
        entry = ctk.CTkEntry(label.master, font=('Segoe UI', 20))
        entry.delete(0, 'end')  # Clear any existing text
        entry.insert(0, original_filename)
        entry.pack(pady=5)
        entry.focus_set()

        def confirm_rename():
            new_filename = entry.get() + os.path.splitext(path)[1]  # Construct new filename
            new_path = os.path.join(os.path.dirname(path), new_filename)
            if os.path.exists(new_path) and new_filename.lower() != os.path.basename(path).lower():
                entry.focus_set()  # If new filename conflicts and exists, refocus to allow re-editing
            else:
                os.rename(path, new_path)  # Rename the file
                label.configure(text=os.path.splitext(new_filename)[0])  # Update the label with new filename
                entry.destroy()  # Destroy the entry widget
                label.pack(pady=5)  # Make sure the label is visible again

                # Update the notes dictionary with the new filename
                old_key = os.path.splitext(os.path.basename(path))[0]
                new_key = os.path.splitext(new_filename)[0]
                if old_key in self.notes:
                    self.notes[new_key] = self.notes.pop(old_key)

                # Save data after renaming
                self.save_data()

        def on_escape(event):
            entry.destroy()  # Destroy the entry widget if escape is pressed
            label.pack(pady=5)  # Repack the label

        entry.bind("<Return>", lambda e: confirm_rename())
        entry.bind("<Escape>", lambda e: on_escape(e))
        entry.bind("<FocusOut>", lambda e: confirm_rename())  # Optional: Rename on focus out

        label.pack_forget()  # Temporarily hide the label while editing

    def rename_images(self):
        if not self.image_folder:
            messagebox.showerror("Error", "No folder loaded.")
            return

        # Prompt for the starting number using CTkInputDialog
        dialog = ctk.CTkInputDialog(title="Enter Starting Number", text="Enter the starting number for renaming:")
        starting_number = dialog.get_input()  # This will block until the dialog is closed
        if starting_number is None or starting_number == "":
            return  # User cancelled the dialog or entered an empty string

        # Check if starting_number is an integer
        try:
            starting_number = int(starting_number)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        try:
            # Helper function to extract numeric parts for sorting
            def numeric_sort_key(path):
                numbers = re.findall(r'\d+', os.path.basename(path))
                return [int(num) for num in numbers]

            # Fetch all image files and sort them
            image_paths = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if
                           f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            image_paths.sort(key=numeric_sort_key)  # Sort files numerically

            # Rename files and update self.notes with new filenames
            updated_notes = {}
            for index, path in enumerate(image_paths, start=starting_number):
                new_name = f"{index:03}{os.path.splitext(path)[1]}"  # Adjust the index to start from starting_number
                new_path = os.path.join(self.image_folder, new_name)
                os.rename(path, new_path)
                old_filename = os.path.splitext(os.path.basename(path))[0]
                new_filename = os.path.splitext(new_name)[0]
                if old_filename in self.notes:
                    updated_notes[new_filename] = self.notes[old_filename]

            # Update self.notes with new filenames
            self.notes = updated_notes

            self.refresh_images()  # Refresh the display to show new filenames

        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename files: {str(e)}")


    def save_data(self):
        # Assuming self.notes stores tags per filename directly
        data = {
            'title': self.title_var.get(),
            'bg_color': self.bg_color,
            'text_color': self.text_color,
            'images': self.notes  # Assuming this structure is correct
        }

        json_path = os.path.join(self.image_folder if self.image_folder else '', 'gallery_data.json')
        try:
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Success", "Data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")


    def load_data(self):
        json_path = os.path.join(self.image_folder if self.image_folder else '', 'gallery_data.json')
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            self.title_var.set(data['title'])
            self.bg_color = data['bg_color']
            self.text_color = data['text_color']
            self.notes = data.get('images', {})  # Load image tags
            self.apply_settings()
            self.display_images(self.image_folder, self.notes)
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved data found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Corrupted data file.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


    def export_json(self, file_data, folder):
        json_path = os.path.join(self.image_folder if self.image_folder else '', folder + '_data.json')
        with open(json_path, 'w') as json_file:
            json.dump(file_data, json_file, indent=4)

        print(f"JSON file has been saved to {json_path}")


    def on_mouse_wheel(self, event):
        # Adjust scrolling depending on the OS
        if self.tk.call('tk', 'windowingsystem') == 'win32':
            # Windows uses 'delta' for the scroll magnitude
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            # macOS uses 'delta', similar to Windows, but often with different sensitivity
            self.canvas.yview_scroll(int(-1 * (event.delta)), "units")


    def save_tag_data(self):
        try:
            with open('tag_colors.json', 'w') as file:
                json.dump(self.tag_colors, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tag data: {str(e)}")

    def load_tag_data(self):
        try:
            with open('tag_colors.json', 'r') as file:
                self.tag_colors = json.load(file)
        except FileNotFoundError:
            self.tag_colors = {}  # Initialize to an empty dict if file doesn't exist
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Tag data file is corrupted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tag data: {str(e)}")


if __name__ == "__main__":
    app = PhotoGalleryApp()
    app.mainloop()
