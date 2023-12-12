import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
from mltu.utils.text_utils import get_cer, get_wer
from tqdm import tqdm
from DataLoading import DataLoading
from GUI import GUI
from ReadImages import ReadImages
from TrainModel import TrainModel

def data_reading(model, df):
    acc_cer, acc_wer = [], []
    for image_path, label in tqdm(df):
        image = cv2.imread(image_path)

        prediction_text = model.predict(image)

        cer = get_cer(prediction_text, label)
        wer = get_wer(prediction_text, label)
        print("Image: ", image_path)
        print("Label:", label)
        print("Prediction: ", prediction_text)
        print(f"CER: {cer}; WER: {wer}")

        acc_cer.append(cer)
        acc_wer.append(wer)

        cv2.imshow(prediction_text, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print(f"Average CER: {np.average(acc_cer)}, Average WER: {np.average(acc_wer)}")

def convet_to_black_and_white(img_path):
    obraz = cv2.imread(img_path)
    obraz_szary = cv2.cvtColor(obraz, cv2.COLOR_BGR2GRAY)
    czarno_bialy_z_wzmacnianiem = cv2.addWeighted(obraz_szary, 1.15, obraz_szary, 0, 0)
    cv2.imwrite(img_path, czarno_bialy_z_wzmacnianiem)


if __name__ == "__main__":

    data_loading = DataLoading()
    dataset, unique_characters, max_text_length, vocab = data_loading.load_data()
    print(unique_characters)
    print(vocab)
    print(max_text_length)
    print(tf.config.list_physical_devices('GPU'))

    train_model = TrainModel(dataset, unique_characters, max_text_length, vocab)

    #model_path = "Model"
    #model = ReadImages(vocab=vocab, model_path=model_path)
    #df = pd.read_csv("Test Data/val.csv").values.tolist()
    #data_reading(model, df)

    #image_path = "C:\---Mati---\Moje Programy\ScribbleScan - Engineering thesis\Data\PolishWords\img01.png"
    #convet_to_black_and_white(image_path)
    #image = cv2.imread(image_path)
    #prediction_text = model.predict(image)
    #print("Prediction: ", prediction_text)

    #app = GUI(vocab)
    #app.run()
