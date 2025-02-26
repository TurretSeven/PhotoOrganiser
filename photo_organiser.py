
import shutil
import os
from exiftool import ExifToolHelper
import tkinter.messagebox
import customtkinter as ctk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from pathlib import Path


def get_folder_source():
    folder_selected = filedialog.askdirectory()

    if len(folder_selected) > 0:
        source_path.delete('1.0', END)
        source_path.insert('end-1c', folder_selected)

    return None


def get_folder_destination():
    folder_selected = filedialog.askdirectory()

    if len(folder_selected) > 0:
        destination_path.delete('1.0', END)
        destination_path.insert('end-1c', folder_selected)

    return None


def copy_photos():
    for item in output_tree.get_children():
        output_tree.delete(item)

    source_folder = source_path.get('1.0', 'end-1c')
    destination_folder = destination_path.get('1.0', 'end-1c')

    copy_files(source_folder, destination_folder)

    tkinter.messagebox.showinfo("Information", "Finished")

    return None


def copy_files(root_source, root_destination):
    file_ext = (".tif", "jpg", "jpeg")
    item_count = 0

    for dir_name, sub_dir_list, file_list in os.walk(root_source):
        for file_name in file_list:
            if ".@__thumb" not in dir_name:
                if ".DS_Store" not in file_name and (file_name.casefold().endswith(file_ext)):
                    source_file_path = os.path.join(dir_name, file_name)

                    # Read the date created/taken from the file
                    ymd = get_ymd(str(source_file_path))

                    # Create destination folder
                    destination_folder = os.path.join(root_destination, ymd[0], ymd[1], ymd[2])
                    Path(str(destination_folder)).mkdir(parents=True, exist_ok=True)

                    # Copy file
                    output_tree.insert('', item_count, text="", values=[f"{destination_folder}/{file_name}"])
                    item_count += 1
                    output_tree.update()

                    shutil.copy2(str(source_file_path), str(destination_folder))

    return None


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
    ext_dic = {}

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ctk.CTk()

    app.title("Photo Organiser")
    app.geometry("800x450")
    app.update()
    app.minsize(app.winfo_width(), app.winfo_height())
    app.resizable(TRUE, FALSE)

    # Frames
    source_frame = ctk.CTkFrame(master=app, height=50, fg_color="transparent")
    source_frame.pack(side=TOP, fill="x")

    dest_frame = ctk.CTkFrame(master=app, height=50, fg_color="transparent")
    dest_frame.pack(side=TOP, fill="x")

    tree_frame = ctk.CTkFrame(master=app, height=400, fg_color="transparent")
    tree_frame.pack(side=TOP, fill="both", expand=True)

    bottom_frame = ctk.CTkFrame(master=app, height=30, fg_color="transparent")
    bottom_frame.pack(side=TOP, fill="both")

    # Source label
    source_label = ctk.CTkLabel(master=source_frame, text="Source:        ")
    source_label.pack(side=LEFT, padx=10, pady=10, anchor=N)

    # Source path textbox
    source_path = ctk.CTkTextbox(master=source_frame, width=650, height=30, wrap="none")
    source_path.bind("<Key>", lambda e: "break")
    source_path.pack(side=LEFT, expand=True, fill='x', pady=10, anchor=NW)

    # Source browse button
    source_browse_button = ctk.CTkButton(master=source_frame, text="...", width=1, command=get_folder_source)
    source_browse_button.pack(side=RIGHT, padx=10, pady=11, anchor=NE)

    # Destination label
    destination_label = ctk.CTkLabel(master=dest_frame, text="Destination: ")
    destination_label.pack(side=LEFT, padx=10, pady=10, anchor=N)

    # Destination path textbox
    destination_path = ctk.CTkTextbox(master=dest_frame, width=650, height=30, wrap="none")
    destination_path.bind("<Key>", lambda e: "break")
    destination_path.pack(side=LEFT, expand=True, fill='x', pady=10, anchor=NW)

    # Destination browse button
    destination_browse_button = ctk.CTkButton(master=dest_frame, text="...", width=1, command=get_folder_destination)
    destination_browse_button.pack(side=RIGHT, padx=10, pady=11, anchor=NE)

    # Output treeview
    output_tree = Treeview(master=tree_frame)
    output_tree['show'] = 'headings'

    # Define the number of columns, column details and header
    output_tree["columns"] = "Copy_Photo"
    output_tree.column("Copy_Photo", width=750, minwidth=350, anchor="w")
    output_tree.heading("Copy_Photo", text="Copying Photo")
    output_tree.pack(side=LEFT, padx=10, anchor=NW, fill="both", expand=True)

    # Run button
    destination_browse_button = ctk.CTkButton(master=bottom_frame, text="Run", width=1, command=copy_photos)
    destination_browse_button.pack(side=RIGHT, padx=10, pady=11, anchor=SE)

    app.mainloop()
