
class DataLoading:

    def __init__(self):
        self.polish_words_img_path = "Data/PolishWords"
        self.polish_words_img_txt = "Data/polishwords.txt"

        self.english_words_img_path = "Data/Sentences"
        self.english_words_img_txt = "Data/sentences.txt"

    def prepare_english_data(self):
        english_images_paths_and_labels = []
        english_text = set()
        max_label_len = 0

        with open(self.english_words_img_txt, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.split(' ')
            if parts[2] == "err":
                continue
            folder_name1 = parts[0][:3]
            folder_name2 = "-".join(parts[0].split('-')[:2])
            image_name = parts[0] + ".png"
            label = parts[-1].rstrip("\n")
            label = label.replace("|", " ")
            path = self.english_words_img_path + "/" + folder_name1 + "/" + folder_name2 + "/" + image_name
            max_label_len = max(max_label_len, len(label))
            english_text.update(list(label))
            english_images_paths_and_labels.append([path, label])

        return english_images_paths_and_labels, english_text, max_label_len

    def prepare_polish_data(self):
        polish_images_paths_and_labels = []
        polish_text = set()
        max_label_len = 0

        with open(self.polish_words_img_txt, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(' ', 1)
            path = self.polish_words_img_path + "/" + f"{parts[0]}.png"
            label = parts[1]
            max_label_len = max(max_label_len, len(label))
            polish_text.update(list(label))
            polish_images_paths_and_labels.append([path, label])

        return polish_images_paths_and_labels, polish_text, max_label_len


    def load_data(self):
        polish_dataset, polish_text, max_polish_text_len = self.prepare_polish_data()
        english_dataset, english_text, max_english_text_len = self.prepare_english_data()

        dataset = []
        dataset.extend(polish_dataset)
        dataset.extend(english_dataset)

        unique_characters = set()
        unique_characters = unique_characters.union(polish_text, english_text)
        max_text_length = max(max_polish_text_len, max_english_text_len)
        unique_characters = sorted(unique_characters)
        vocab = "".join(unique_characters)

        return dataset, unique_characters, max_text_length, vocab