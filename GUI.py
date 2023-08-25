import os.path
import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk, ImageDraw, ImageFont
from autocorrect import Speller
from ReadImages import ReadImages

class GUI:
    def __init__(self, vocab):
        self.window = tk.Tk()
        self.window.title("ScribbleScan")
        self.window.geometry("800x350")
        self.vocab = vocab

        self.current_page = None

    def run(self):
        self.show_select_img_page()
        self.window.mainloop()

    def show_select_img_page(self):
        self.hide_current_page()
        self.current_page = SelectImgPage(self.window, self)
        self.current_page.show()

    def show_img_and_text_page(self, img_path, selected_language):
        self.hide_current_page()
        self.current_page = ImgAndTextPage(self.window, self, img_path, self.vocab, selected_language)
        self.current_page.show()

    def show_corrected_img_and_text(self, img_path, text_from_img, selected_language):
        self.hide_current_page()
        self.current_page = CorrectedImgAndText(self.window, self, img_path, text_from_img, selected_language)
        self.current_page.show()

    def hide_current_page(self):
        if self.current_page:
            self.current_page.hide()

class Page:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.frame = tk.Frame(self.parent)

    def show(self):
        self.frame.pack()
        self.frame.tkraise()

    def hide(self):
        self.frame.pack_forget()

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

        values = ['English', 'Polish']
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

class ImgAndTextPage(Page):
    def __init__(self, parent, controller, img_path, vocab, selected_language):
        super().__init__(parent, controller)

        self.img_path = img_path
        self.vocab = vocab
        self.selected_language = selected_language
        self.image = Image.open(img_path)
        self.img_width, self.img_height = self.image.size

        if self.img_width < 700:
            self.img_width = self.img_width + 400
        else:
            self.img_width = self.img_width

        if self.img_height < 200:
            self.img_height = self.img_height + 400
        else:
            self.img_height = self.img_height

        parent.geometry(f"{self.img_width}x{self.img_height}")
        self.image.thumbnail((800, 700))
        self.photo = ImageTk.PhotoImage(self.image)

        model_path = "Model"
        model = ReadImages(vocab=self.vocab, model_path=model_path)
        self.text_from_img = self.read_img(model, self.img_path)

        self.image_label = tk.Label(self.frame, image=self.photo)
        self.image_label.pack(side="left", padx=20, pady=20)

        self.text_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.text_frame, text="Text read from the picture \n(If there are any mistakes you can change this text): ", font=("Helvetica", 10))
        self.label.pack(pady=20)
        self.text_widget = tk.Text(self.text_frame, height=20, width=40, wrap=tk.WORD)
        self.text_widget.pack()
        self.text_widget.insert("1.0", self.text_from_img)
        self.text_frame.pack(side="left", padx=20)

        self.button_frame = tk.Frame(self.text_frame)
        self.back_button = tk.Button(self.button_frame, text="Go Back", bg="#C1C1CD", command=self.go_back)
        self.back_button.pack(side="left", pady=10, padx=5)
        self.next_button = tk.Button(self.button_frame, text="Go Next", bg="#C1C1CD", command=self.go_next)
        self.next_button.pack(side="left", pady=10, padx=5)
        self.button_frame.pack()

    def read_img(self, model, img_path):
        image = cv2.imread(img_path)
        predicted_text = model.predict(image)

        return predicted_text

    def go_back(self):
        self.controller.show_select_img_page()

    def go_next(self):
        self.corrected_text = self.text_widget.get("1.0", "end-1c")
        self.controller.show_corrected_img_and_text(self.img_path, self.corrected_text, self.selected_language)

class CorrectedImgAndText(Page):
    def __init__(self, parent, controller, img_path, text, selected_language):
        super().__init__(parent, controller)

        self.img_path = img_path
        self.text = text
        self.selected_language = selected_language
        self.image = Image.open(img_path)
        self.img_width, self.img_height = self.image.size

        if self.img_width < 700:
            self.img_width = self.img_width + 400
        else:
            self.img_width = self.img_width

        if self.img_height < 200:
            self.img_height = self.img_height + 400
        else:
            self.img_height = self.img_height

        parent.geometry(f"{self.img_width}x{self.img_height}")

        self.marked_photo = self.mark_errors()

        self.image_label = tk.Label(self.frame, image=self.marked_photo)
        self.image_label.pack(side="left", padx=20, pady=20)

        self.main_frame = tk.Frame(self.frame)

        self.label = tk.Label(self.main_frame, text="Text with corrected words: ", font=("Helvetica", 10, "bold"))
        self.label.pack(pady=20)

        corrected_text, corrected_words = self.correct_text_with_errors()
        self.text_label1 = tk.Label(self.main_frame, text=corrected_text, font=("Helvetica", 12))
        self.text_label1.pack(padx=20, pady=20)
        self.main_frame.pack(side="left", padx=20)

        self.inner_frame = tk.Frame(self.main_frame)
        self.label = tk.Label(self.inner_frame, text="Corrections that were made: ", font=("Helvetica", 10, "bold"))
        self.label.pack(pady=20)
        corrections = "\n".join([f"{wrong_word} -> {corrected_word}" for wrong_word, corrected_word in corrected_words])
        self.text_label2 = tk.Label(self.inner_frame, text=corrections, font=("Helvetica", 12))
        self.text_label2.pack(padx=10, pady=10)
        self.inner_frame.pack()

        self.button_frame = tk.Frame(self.main_frame)
        self.back_button = tk.Button(self.button_frame, text="Home", command=self.go_home)
        self.back_button.pack(pady=10)
        self.button_frame.pack()

    def go_home(self):
        self.controller.show_select_img_page()

    def mark_errors(self):
        img = cv2.imread(self.img_path)
        lang = None

        if self.selected_language == "English":
            lang = "en"
        elif self.selected_language == "Polish":
            lang = "pl"

        spell = Speller(lang=lang)

        words = self.text.split()

        rectangles = self.find_coordinates_of_misspelled_word(self.img_path)

        for word, rect_coords in zip(words, rectangles):
            corrected_word = spell(word)
            if word != corrected_word:
                x, y, w, h = rect_coords
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, corrected_word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img.thumbnail((800, 700))
        return ImageTk.PhotoImage(img)

    def find_coordinates_of_misspelled_word(self, img_path):
        image_cv = cv2.imread(img_path)
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=6)

        contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

        rectangles = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            rectangles.append((x, y, w, h))

        return rectangles

    def correct_text_with_errors(self):
        lang = None

        if self.selected_language == "English":
            lang = "en"
        elif self.selected_language == "Polish":
            lang = "pl"

        spell = Speller(lang=lang)

        words = self.text.split()
        corrected_words = []
        for i, word in enumerate(words):
            corrected_word = spell(word)
            if word != corrected_word:
                words[i] = corrected_word
                corrected_words.append((word, corrected_word))

        corrected_text = " ".join(words)
        return corrected_text, corrected_words

