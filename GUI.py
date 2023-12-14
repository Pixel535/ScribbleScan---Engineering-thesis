import tkinter as tk
from GUI_CorrectedImgAndText import CorrectedImgAndText
from GUI_ImgAndTextPage import ImgAndTextPage
from GUI_SelectImgPage import SelectImgPage


class GUI_Class:
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
