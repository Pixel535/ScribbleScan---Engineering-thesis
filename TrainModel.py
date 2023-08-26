import os.path
from mltu.dataProvider import DataProvider
from mltu.preprocessors import ImageReader
from mltu.transformers import ImageResizer, LabelIndexer, LabelPadding
from mltu.augmentors import RandomBrightness, RandomErodeDilate, RandomSharpen
from HTR_Model import HTR_Model
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard, BackupAndRestore
from mltu.callbacks import Model2onnx, TrainLogger
import tensorflow as tf
try: [tf.config.experimental.set_memory_growth(gpu, True) for gpu in tf.config.experimental.list_physical_devices("GPU")]
except: pass

class TrainModel:
    def __init__(self, dataset, unique_characters, max_text_length, vocab):
        self.width = 1500
        self.height = 100

        self.dataset = dataset
        self.unique_characters = unique_characters
        self.max_text_length = max_text_length
        self.vocab = vocab

        self.HTR_Model = HTR_Model

        self.trainModel()


    def trainModel(self):
        print("Loading Data...")
        print("Finished Loading Data...")

        print("Creating DataProvider...")

        data_provider = DataProvider(
            dataset=self.dataset,
            skip_validation=True,
            batch_size=16,
            data_preprocessors=[ImageReader()],
            transformers=[
                ImageResizer(self.width, self.height, keep_aspect_ratio=True),
                LabelIndexer(self.vocab),
                LabelPadding(max_word_length=self.max_text_length, padding_value=len(self.vocab)),
            ],
        )

        print("DataProvider Created...")

        print("Creating Model...")

        if os.path.exists("Model/model.h5"):
            img_shape = (self.height, self.width, 3)
            HTR_Model = self.HTR_Model(img_shape, len(self.vocab), self.vocab)
            HTR_Model.compile_model()
            HTR_Model.model.load_weights("Model/model.h5")
            print(HTR_Model.model.get_weights())
            new_model = False
        else:
            img_shape = (self.height, self.width, 3)
            HTR_Model = self.HTR_Model(img_shape, len(self.vocab), self.vocab)
            HTR_Model.compile_model()
            HTR_Model.summary(line_length=110)
            print(HTR_Model.model.get_weights())
            new_model = True

        print("Model Created...")

        print("Training Model...")

        train_ratio = 0.8
        training_data, val_data = data_provider.split(split=train_ratio)
        training_data.augmentors = [
            RandomBrightness(),
            RandomErodeDilate(),
            RandomSharpen(),
        ]

        backup = BackupAndRestore(backup_dir="Model/backup")
        earlystopper = EarlyStopping(monitor='val_CER', patience=20, verbose=1, mode='min')
        checkpoint = ModelCheckpoint("Model/model.h5", monitor='val_CER', verbose=1, save_best_only=True, mode='min')
        trainLogger = TrainLogger("Model")
        tb_callback = TensorBoard('Model/logs', update_freq=1)
        reduceLROnPlat = ReduceLROnPlateau(monitor='val_CER', factor=0.9, min_delta=1e-10, patience=10, verbose=1,
                                           mode='auto')
        model2onnx = Model2onnx("Model/model.h5")

        is_Trained = False

        if is_Trained is False:
            if new_model is True:
                HTR_Model.train(training_data,
                                val_data,
                                epochs=1000,
                                workers=20,
                                callbacks=[backup, earlystopper, checkpoint, trainLogger, reduceLROnPlat, tb_callback, model2onnx])
            else:
                HTR_Model.train(training_data,
                                val_data,
                                epochs=1000,
                                workers=20,
                                callbacks=[backup, earlystopper, checkpoint, trainLogger, reduceLROnPlat, tb_callback, model2onnx])

        print("Finished Training Model...")

        loss, CER, WER = HTR_Model.validate(val_data)

        print("Validation loss: ", loss)
        print("Validation CER: ", CER)
        print("Validation WER: ", WER)

        training_data.to_csv(os.path.join("Test Data", "train.csv"))
        val_data.to_csv(os.path.join("Test Data", "val.csv"))


