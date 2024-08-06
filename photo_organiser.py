
import shutil
import os
import sys
from exiftool import ExifToolHelper
import tkinter.messagebox
import customtkinter as ctk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from pathlib import Path


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Photo Organiser")
        self.geometry("800x550")
        self.resizable(FALSE, FALSE)

        # Source label
        self.source_label = ctk.CTkLabel(self, text="Source: ")
        self.source_label.place(x=10, y=8)

        # Source path textbox
        self.source_path = ctk.CTkTextbox(self, width=670, height=35, wrap="none")
        self.source_path.bind("<Key>", lambda e: "break")
        self.source_path.place(x=90, y=8)

        # Source browse button
        self.source_browse_button = ctk.CTkButton(self, text="...", width=1, command=self.get_folder_source)
        self.source_browse_button.place(x=765, y=10)

        # Destination label
        self.destination_label = ctk.CTkLabel(self, text="Destination: ")
        self.destination_label.place(x=10, y=50)

        # Source path textbox
        self.destination_path = ctk.CTkTextbox(self, width=670, height=35, wrap="none")
        self.destination_path.bind("<Key>", lambda e: "break")
        self.destination_path.place(x=90, y=50)

        # Destination browse button
        self.destination_browse_button = ctk.CTkButton(self, text="...", width=1, command=self.get_folder_destination)
        self.destination_browse_button.place(x=765, y=52)

        # Output treeview
        self.output_tree = Treeview(self)
        self.output_tree['show'] = 'headings'

        # Define the number of columns, column details and header
        self.output_tree["columns"] = "Copy_Photo"
        self.output_tree.column("Copy_Photo", width=750, minwidth=350, anchor="w")
        self.output_tree.heading("Copy_Photo", text="Copying Photo")
        self.output_tree.place(x=10, y=100, width=780, height=402)

        # Run button
        self.destination_browse_button = ctk.CTkButton(self, text="Run", width=1, command=self.copy_photos)
        self.destination_browse_button.place(x=750, y=512)

    def get_folder_source(self):
        folder_selected = filedialog.askdirectory()

        if len(folder_selected) > 0:
            self.source_path.delete('1.0', END)
            self.source_path.insert('end-1c', folder_selected)

        return None

    def get_folder_destination(self):
        folder_selected = filedialog.askdirectory()

        if len(folder_selected) > 0:
            self.destination_path.delete('1.0', END)
            self.destination_path.insert('end-1c', folder_selected)

        return None

    def copy_photos(self):
        for item in self.output_tree.get_children():
            self.output_tree.delete(item)

        source_folder = self.source_path.get('1.0', 'end-1c')
        destination_folder = self.destination_path.get('1.0', 'end-1c')

        self.copy_files(source_folder, destination_folder)

        tkinter.messagebox.showinfo("Information", "Finished")

        return None

    def copy_files(self, root_source, root_destination):
        file_ext = (".tif", "jpg", "jpeg")
        item_count = 0

        for dir_name, sub_dir_list, file_list in os.walk(root_source):
            for file_name in file_list:
                if ".@__thumb" not in dir_name:
                    if ".DS_Store" not in file_name and (file_name.casefold().endswith(file_ext)):
                        source_file_path = os.path.join(dir_name, file_name)

                        # Read the date created/taken from the file
                        ymd = self.get_ymd(str(source_file_path))

                        # Create destination folder
                        destination_folder = os.path.join(root_destination, ymd[0], ymd[1], ymd[2])
                        Path(str(destination_folder)).mkdir(parents=True, exist_ok=True)

                        # Copy file
                        self.output_tree.insert('', item_count, text="",
                                                values=[f"{destination_folder}/{file_name}"])
                        item_count += 1
                        self.output_tree.update()

                        shutil.copy2(str(source_file_path), str(destination_folder))

        return None

    @staticmethod
    def get_ymd(file_path: str) -> tuple:
        date_created = "0:0:0"

        try:
            with ExifToolHelper() as et:
                meta_data = et.get_tags([file_path], tags=["EXIF:DateTimeOriginal"])

            if len(meta_data) == 1:
                date_time_original = meta_data[0]["EXIF:DateTimeOriginal"]

                if ":" in date_time_original:
                    date_created = date_time_original[:10]
        except IndexError:
            print(f"An exception has been raised on [{file_path}].")

        image_date = date_created.split(':')

        return image_date[0], image_date[1], image_date[2]


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()
    sys.exit(0)
