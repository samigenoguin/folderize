import os, shutil, time, threading
from pathlib import Path
import tkinter as tk
from  tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk 

# welcome window; runs first
class WelcomeWindow:
    def __init__(self):
        self.theme = "flatly"
        self.window = ttk.Window(themename=self.theme)
        self.window.title("Folderize")
        self.window.geometry("380x320")
        self.window.resizable(False, False)

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.configure_styles()
        self.add_widgets()
        self.place_window()
    
    # configure default style
    def configure_styles(self):
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11))

    # add widgets to the window
    def add_widgets(self):
        # for the folder icon
        self.logo_path = os.path.join(self.base_path, "icon.png")
        self.logo = Image.open(self.logo_path)
        self.logo = self.logo.resize((100,100))
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = ttk.Label(self.window, image=self.logo, compound="top")
        self.logo_label.pack(pady=20)

        # add title heading
        self.heading1 = ttk.Label(self.window, text="Folderize", font="Arial 22 bold")
        self.heading1.place(relx=0.5, y=160, anchor="center")

        # add subtitle
        self.subtitle = ttk.Label(
            self.window,
            text="Simplify your workflow by sorting files into their proper places automatically",
            font="Arial 11",
            wraplength=320,
            justify="center"
        )
        self.subtitle.place(relx=0.5, y=210, anchor="center")

        # buttons
        self.buttons_frame = ttk.Frame(self.window)
        self.button1 = ttk.Button(self.buttons_frame, text="Documentation", bootstyle="secondary")
        self.button2 = ttk.Button(self.buttons_frame, text="Run App", bootstyle="info", command=self.open_entry_window)

        self.buttons_frame.place(relx=0.5, y=270, anchor="center")
        self.button1.pack(side="left", padx=10)
        self.button2.pack(side="left", padx=10)

    # update position
    def update_position(self):
        self.window.update_idletasks()
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()
        self.x = self.window.winfo_x()
        self.y = self.window.winfo_y()

    # callback for "Run App" button
    def open_entry_window(self):
        self.update_position()
        entry_window = EntryWindow(self)

    # display window
    def display(self):
        self.window.mainloop()

    # center window when pops
    def place_window(self):
        self.window.update_idletasks()

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        x = (self.screen_width // 2) - (window_width // 2)
        y = (self.screen_height // 2) - (window_height // 2)

        self.window_width = window_width
        self.window_height = window_height
        self.x = x
        self.y = y

        self.window.geometry(f"{window_width}x{window_height}+{self.x}+{self.y}")

# entry window; runs when "Run App" is clicked
class EntryWindow:
    def __init__(self, parent):
        self.parent = parent
        self.theme = "flatly"
        self.window = tk.Toplevel(self.parent.window)
        self.window.title("Folderize")
        self.window.geometry("380x150")
        self.window.resizable(False, False)

        self.path_var = ttk.StringVar()

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.window.transient(self.parent.window)
        self.window.grab_set()
        self.add_widgets()
        self.place_window()

    # add widgets to the window
    def add_widgets(self):
        self.entry_label = ttk.Label(self.window, text="Enter a path or browse:", font="Arial 11")
        self.entry = ttk.Entry(self.window, width=50, textvariable=self.path_var)

        self.buttons_frame = ttk.Frame(self.window)
        self.browse_button = ttk.Button(self.buttons_frame, text="Browse", bootstyle="secondary", command=self.browse_folder)
        self.run_button = ttk.Button(self.buttons_frame, text="Run", bootstyle="info", command=self.run_folderize)

        self.entry_label.place(x=33, y=15)
        self.entry.place(relx=0.5, anchor="center", y=60)
        self.buttons_frame.place(x=33, y=93)
        self.browse_button.pack(side="left", padx=(0,10))
        self.run_button.pack(side="left")

    # allow user to browse folder
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path: self.path_var.set(folder_path)

    # callback for run button
    def run_folderize(self):
        working_path = Path(self.path_var.get().strip())
        print(f"selected_path: {working_path}")

        # validate the given path
        if not working_path.exists() or not working_path.is_dir():
            self.display_error("Either given path is not a folder or does not exists.")
            return

        # getting files
        files = [file for file in working_path.iterdir() if file.is_file()]
        if not files:
            self.display_error("No files found in the given folder")
            return
        
        progress_window = ProgressWindow(self)

    # display error popup
    def display_error(self, message):
        Messagebox.show_info(message, "Warning", parent=self.window)
        self.window.grab_set()

    # center window when pops
    def place_window(self):
        self.window.update_idletasks()

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()

        parent_x = self.parent.x
        parent_y = self.parent.y
        parent_width = self.parent.window_width

        x = parent_x + parent_width + 20
        y = parent_y

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# display progress
class ProgressWindow:
    def __init__(self, parent):
        self.parent = parent
        self.path_var = self.parent.path_var
        self.status_var = ttk.StringVar(value="Folderizing..")

        # create a popup for the progress
        self.window = ttk.Toplevel(self.parent.window)
        self.window.geometry("380x130")
        self.window.title("Progress")
        self.window.resizable(False, False)
        
        self.main_label = ttk.Label(self.window, textvariable=self.status_var, font="arial 11", justify="center")
        self.main_label.pack(pady=20)

        self.progressbar = ttk.Progressbar(
            self.window, 
            orient="horizontal",
            length=300,
            mode="determinate",
            bootstyle="info"
            )
        self.progressbar.pack()

        self.place_window()

        # start the function in a thread
        threading.Thread(target=self.folderize_and_finish, daemon=True).start()

    # main function
    def folderize(self):
        working_path = Path(self.path_var.get().strip())
        files = [file for file in working_path.iterdir() if file.is_file()]

        # iterating to the files
        total_files = len(files)
        self.progressbar["maximum"] = total_files

        for i, file in enumerate(files, start=1):
            extension = file.suffix[1:] if file.suffix else "OTHERS"
            target_folder = working_path / extension

            # create a folder if it does not exist
            target_folder.mkdir(exist_ok=True)

            # move file to respective extension
            shutil.move(str(file), str(target_folder / file.name))
            print(f"Moved {file.name} -> {target_folder}")

            self.window.after(0, lambda i=i: self.update_progress(i, len(files)))
            time.sleep(0.05)

    def update_progress(self, current, total):
        self.status_var.set(f"Folderizing {current}/{total} files..")
        self.progressbar["value"] = current

    # function to run folderize and add success text
    def folderize_and_finish(self):
        self.folderize()
        self.window.after(0, lambda: self.status_var.set(f"Path successfully folderized!"))
        self.countdown_and_destroy(6)

    # countdown before close the window
    def countdown_and_destroy(self, remaining):
        if remaining > 0:
            self.status_var.set(f"Will close in {remaining}...")
            self.window.after(1000, lambda: self.countdown_and_destroy(remaining - 1))
        else:
            self.window.destroy()

    # place window properly when popup
    def place_window(self):
        self.window.update_idletasks()
        window_height = self.window.winfo_height()
        window_width = self.window.winfo_width()
        
        parent_x = self.parent.window.winfo_x()
        parent_y = self.parent.window.winfo_y()
        parent_height = self.parent.window.winfo_height()

        x = parent_x
        y = parent_y + parent_height + 50

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# run the app
if __name__ == "__main__":
    welcome_window = WelcomeWindow()
    welcome_window.display()