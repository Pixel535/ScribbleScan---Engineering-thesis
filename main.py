import tensorflow as tf
from DataLoading import DataLoading
from GUI import GUI
from Graphs import Graphs
from TrainModel import TrainModel

if __name__ == "__main__":

    is_model_trained = True

    data_loading = DataLoading()
    dataset, unique_characters, max_text_length, vocab = data_loading.load_data()

    print(unique_characters)
    print(vocab)
    print(max_text_length)
    print(tf.config.list_physical_devices('GPU'))

    if not is_model_trained:
        train_model = TrainModel(dataset, unique_characters, max_text_length, vocab)
    else:
        logs_path = "Model/logs.log"
        Graphs(logs_path)

        app = GUI(vocab)
        app.run()


