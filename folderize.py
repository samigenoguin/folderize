import os
import shutil

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import filedialog

# set window
window = ttk.Window(themename="darkly")
window.title("File Organizer")
window.geometry("420x195")
window.resizable(False, False)

# setting path
path_var = tk.StringVar()
status_var = tk.StringVar()
status_var.set("...")

# browse function
def browse_folder():
	folder = filedialog.askdirectory()
	if folder:
		path_var.set(folder)

# list and filters file
def get_files(directory):
	files_and_dirs = os.listdir(directory)
	files = [file for file in files_and_dirs if os.path.isfile(os.path.join(directory, file))]
	return files

# get the file extensions without "."
def get_extension(file):
	extension = os.path.splitext(file)[1]
	return extension[1:].upper() if extension else "OTHERS"

# move the file to its respective extension
def move_file(file, src_folder, extension):
    src = os.path.join(src_folder, file)
    dst_folder = os.path.join(src_folder, extension)

    # make sure the folder exists
    os.makedirs(dst_folder, exist_ok=True)
    dst = os.path.join(dst_folder, file)
    shutil.move(src, dst)
	
    print(f"Moved {file} → {dst_folder}")

# check if a folder exists already
def is_exists(folder):
	exists = os.path.exists(folder)
	return exists

# create a folder
def create_folder(foldername):
	os.makedirs(foldername, exist_ok=True)
	print(f"folder {foldername} created")

# get the current file name
def get_working_file():
	current_file = os.path.abspath(__file__)
	return current_file

# main function to run
def organize():
	path = path_var.get().strip()
	folder_exists = is_exists(path)

	# run if exists
	if folder_exists:
		files = get_files(path)
		working_file =  get_working_file()

		# loop through the folder
		moved_files = 0
		for file in files:
			if os.path.abspath(file) != working_file:
				extension = get_extension(file)

				# create a folder if not exists
				if not is_exists(extension):
					create_folder(extension)

				move_file(file, path, extension)
				moved_files += 1
				status_var.set(f"Organizing files.. {moved_files}/{len(files)}")

		status_var.set(f"Files successfully organized {len(files)} files!")

	# else, error
	if not folder_exists:
		status_var.set(f"The system cannot find the path specified")

# style
style = ttk.Style()
style.configure("Italic.TButton", font=("Arial", 10, "italic"))

# label
label = ttk.Label(window, text="Select a folder to organize:", font="Arial 10 italic bold")
label.place(x=53, y=20)

# Entry
entry = ttk.Entry(window, textvariable=path_var, width=50)
entry.place(x=53, y=55)

# text
status_text = ttk.Label(window, textvariable=status_var, text="...", font="arial 10 italic", wraplength=350, justify="left")
status_text.place(x=53, y=100)

# Buttons
browse_button = ttk.Button(window, text="Browse", command=browse_folder, style="Italic.TButton")
browse_button.place(x=53, y=135)

main_button = ttk.Button(window, text="Run", command=organize, style="Italic.TButton")
main_button.place(x=123, y=135)

# run when called
if __name__ == "__main__":
	window.mainloop()