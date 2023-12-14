import tkinter as tk
import cv2
import numpy as np
from GUI_CorrectedImgAndText import CorrectedImgAndText
from GUI_ImgAndTextPage import ImgAndTextPage
from GUI_SelectImgPage import SelectImgPage


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


def split_lines(image_path):
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
