import tkinter as tk
from GUI_Page import Page
from tkinter import filedialog, ttk
import os.path


class SelectImgPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.parent = parent
        parent.geometry("800x500")

        # ----- Info Labels -----
        self.label = tk.Label(self.frame, text="Welcome to ScribbleScan !", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=20)
        self.info = tk.Label(self.frame,
                             text="Select an image with your notes and the application will show "
                                  "\nwhere the spelling mistakes are and provide corrections",
                             font=("Helvetica", 10, "bold"))
        self.info.pack(pady=20)

        # ----- Error Label -----
        self.error_label1 = tk.Label(self.frame, text="", fg="red")
        self.error_label1.pack()

        # ----- Button 1 -----
        self.load_button = tk.Button(self.frame, text="Choose .png or .jpg file: ", bg="#C1C1CD", command=self.load_image)
        self.load_button.pack(pady=10)

        # ----- Button Labels -----
        self.TextFrame = tk.Frame(self.frame)
        self.selected_img_label = tk.Label(self.TextFrame, text="Choosen File: ", font=("Helvetica", 10))
        self.selected_img_label.pack(side="left", pady=5)
        self.selected_img_name = tk.Label(self.TextFrame, text="", font=("Helvetica", 10, 'bold'))
        self.selected_img_name.pack(side="left", pady=5)
        self.TextFrame.pack()

        # ----- ComboBox and Labels -----
        self.error_label2 = tk.Label(self.frame, text="", fg="red")
        self.error_label2.pack()

        self.combo_box_text = tk.Label(self.frame, text="Select the language in which the notes are written: ")
        self.combo_box_text.pack()

        self.combo_value = tk.StringVar()

        values = ['English US', 'English GB', 'Polish']
        self.combo_box = ttk.Combobox(self.frame, textvariable=self.combo_value, state='readonly', values=values)
        self.combo_box.pack()
        self.selected_language = None

        # ----- Button 2 -----
        self.go_next_button = tk.Button(self.frame, text="Go next", bg="#C1C1CD", command=self.go_next)
        self.go_next_button.pack(pady=20)

        self.selected_file_path = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.selected_img_name.config(text=f"{file_name}")

    def go_next(self):
        self.selected_language = self.combo_box.get()
        if self.selected_file_path and self.selected_language is not None and self.selected_language != '':
            self.error_label1.config(text="")
            self.error_label2.config(text="")
            self.controller.show_img_and_text_page(self.selected_file_path, self.selected_language)
        else:
            if not self.selected_file_path:
                self.error_label1.config(text="You have to choose a file !")
            else:
                self.error_label1.config(text="")
            if self.selected_language is None or self.selected_language == '':
                self.error_label2.config(text="You have to select language !")
            else:
                self.error_label2.config(text="")