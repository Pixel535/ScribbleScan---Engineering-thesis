import tkinter as tk
from GUI import split_lines
from GUI_Page import Page
from PIL import Image, ImageTk
import enchant
import cv2


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

        # Mark photo with rectangles if there is an error
        self.marked_photo = self.mark_errors()

        self.image_label = tk.Label(self.frame, image=self.marked_photo)
        self.image_label.pack(side="left", padx=20, pady=20)

        # Create frame and its labels
        self.main_frame = tk.Frame(self.frame)

        self.label = tk.Label(self.main_frame, text="Text with corrected words: ", font=("Helvetica", 10, "bold"))
        self.label.pack(pady=20)

        # Labels for corrected text and mistakes that have been found
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

        # Buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.back_button = tk.Button(self.button_frame, text="Home", command=self.go_home)
        self.back_button.pack(pady=10)
        self.button_frame.pack()

    def go_home(self):
        self.controller.show_select_img_page()

    def mark_errors(self):
        lang = None

        if self.selected_language == "English US":
            lang = "en_US"
        elif self.selected_language == "English GB":
            lang = "en_GB"
        elif self.selected_language == "Polish":
            lang = "pl_PL"

        dictionary = enchant.DictWithPWL(lang)

        line_texts = self.text.split('\n')
        lines = split_lines(self.img_path)

        corrected_images = []

        for line, line_text in zip(lines, line_texts):
            words = line_text.split()
            rectangles = self.find_coordinates_of_misspelled_word(line)
            for word, rect_coords in zip(words, rectangles):
                if not dictionary.check(word):
                    suggestions = dictionary.suggest(word)
                    corrected_word = suggestions[0] if suggestions else word
                    x, y, w, h = rect_coords
                    cv2.rectangle(line, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(line, corrected_word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
            corrected_images.append(line)

        combined_image = cv2.vconcat(corrected_images)
        img = Image.fromarray(cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB))
        img.thumbnail((800, 700))
        return ImageTk.PhotoImage(img)

    def find_coordinates_of_misspelled_word(self, line):
        rectangles = []
        gray = cv2.cvtColor(line, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 5)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 8)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=6)

        contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            max_distance = 20

            updated = False
            for i, rect in enumerate(rectangles):
                rx, ry, rw, rh = rect

                # if rectangle is touching other rectangle
                if ((rx <= x <= rx + rw or rx <= x + w <= rx + rw) and (ry <= y <= ry + rh or ry <= y + h <= ry + rh)):
                    rectangles[i] = (min(x, rx), min(y, ry), max(x + w, rx + rw) - min(x, rx), max(y + h, ry + rh) - min(y, ry))
                    updated = True
                    break

                # if rectangle is really close to other rectangle
                if ((x >= rx - max_distance and x <= rx + rw + max_distance and y >= ry - max_distance and y <= ry + rh + max_distance) or
                     (x + w >= rx - max_distance and x + w <= rx + rw + max_distance and y >= ry - max_distance and y <= ry + rh + max_distance) or
                     (x >= rx - max_distance and x <= rx + rw + max_distance and y + h >= ry - max_distance and y + h <= ry + rh + max_distance) or
                     (x + w >= rx - max_distance and x + w <= rx + rw + max_distance and y + h >= ry - max_distance and y + h <= ry + rh + max_distance)):
                    rectangles[i] = (min(x, rx), min(y, ry), max(x + w, rx + rw) - min(x, rx), max(y + h, ry + rh) - min(y, ry))
                    updated = True
                    break

                # if rectangle has crossed  other rectangle
                if ((rx < x < rx + rw or x < rx < x + w) and (ry < y < ry + rh or y < ry < y + h)):
                    rectangles[i] = (min(x, rx), min(y, ry), max(x + w, rx + rw) - min(x, rx), max(y + h, ry + rh) - min(y, ry))
                    updated = True
                    break

                # if rectangle is inside other rectangle
                if (rx <= x and ry <= y and rx + rw >= x + w and ry + rh >= y + h):
                    updated = True
                    break

                # if rectangle has other rectangle inside
                if (x <= rx and y <= ry and x + w >= rx + rw and y + h >= ry + rh):
                    rectangles[i] = (x, y, w, h)
                    updated = True
                    break

            if not updated:
                rectangles.append((x, y, w, h))

        return rectangles

    def correct_text_with_errors(self):
        lang = None

        if self.selected_language == "English US":
            lang = "en_US"
        elif self.selected_language == "English GB":
            lang = "en_GB"
        elif self.selected_language == "Polish":
            lang = "pl_PL"

        dictionary = enchant.DictWithPWL(lang)

        lines = self.text.split('\n')
        corrected_words = []
        corrected_lines = []

        for line in lines:
            words = line.split()
            for i, word in enumerate(words):
                if not dictionary.check(word):
                    suggestions = dictionary.suggest(word)
                    corrected_word = suggestions[0] if suggestions else word
                    words[i] = corrected_word
                    corrected_words.append((word, corrected_word))
            corrected_line = " ".join(words)
            corrected_lines.append(corrected_line)

        corrected_text = "\n".join(corrected_lines)

        return corrected_text, corrected_words