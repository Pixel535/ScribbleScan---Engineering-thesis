import tkinter as tk
from GUI_Page import Page
from PIL import Image, ImageTk
from ReadImages import ReadImages
import cv2
import numpy as np

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

        if self.img_width > 1800:
            self.img_width = 1750

        if self.img_height < 450:
            self.img_height = self.img_height + 400
        else:
            self.img_height = self.img_height

        if self.img_height > 800:
            self.img_height = 800

        # Resolution depends on img
        parent.geometry(f"{self.img_width}x{self.img_height}")
        self.image.thumbnail((800, 700))
        self.photo = ImageTk.PhotoImage(self.image)

        # Reading text from img
        model_path = "Model"
        model = ReadImages(vocab=self.vocab, model_path=model_path)
        self.text_from_img = self.read_img(model, self.img_path)

        # img
        self.image_label = tk.Label(self.frame, image=self.photo)
        self.image_label.pack(side="left", padx=20, pady=20)

        # Text label and text that can be changed
        self.text_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.text_frame,
                              text="Text read from the picture \n(If there are any mistakes you can change this text): ",
                              font=("Helvetica", 10))
        self.label.pack(pady=20)
        self.text_widget = tk.Text(self.text_frame, height=20, width=40, wrap=tk.WORD)
        self.text_widget.pack()
        self.text_widget.insert("1.0", self.text_from_img)
        self.text_frame.pack(side="left", padx=20)

        # Buttons
        self.button_frame = tk.Frame(self.text_frame)
        self.back_button = tk.Button(self.button_frame, text="Go Back", bg="#C1C1CD", command=self.go_back)
        self.back_button.pack(side="left", pady=10, padx=5)
        self.next_button = tk.Button(self.button_frame, text="Go Next", bg="#C1C1CD", command=self.go_next)
        self.next_button.pack(side="left", pady=10, padx=5)
        self.button_frame.pack()

    def read_img(self, model, img_path):
        lines = self.split_lines(img_path)
        predicted_text = ""
        for line in lines:
            predicted_line = model.predict(line)
            predicted_text += predicted_line + "\n"

        return predicted_text

    def go_back(self):
        self.controller.show_select_img_page()

    def go_next(self):
        self.corrected_text = self.text_widget.get("1.0", "end-1c")
        self.controller.show_corrected_img_and_text(self.img_path, self.corrected_text, self.selected_language)

    def split_lines(self, image_path):
        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, bin_img = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

        px_avg = np.mean(bin_img, axis=1)

        threshold = 0
        histogram = px_avg <= threshold

        y_coords = []

        y = 0
        count = 0
        is_space = False

        for i in range(len(histogram)):
            if not is_space:
                if histogram[i]:
                    is_space = True
                    count = 1
                    y = i
            else:
                if not histogram[i]:
                    is_space = False
                    y_coords.append(y // count)
                else:
                    y += i
                    count += 1

        lines = []
        if len(y_coords) != 0:
            for i in range(len(y_coords) - 1):
                line = image[y_coords[i]:y_coords[i + 1], :]
                lines.append(line)
            lines.append(image[y_coords[-1]:, :])
        else:
            lines.append(image)
        return lines