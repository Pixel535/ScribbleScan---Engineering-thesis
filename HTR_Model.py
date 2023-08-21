import tensorflow as tf
from mltu.losses import CTCloss
from mltu.metrics import CERMetric, WERMetric
from mltu.model_utils import residual_block
from keras import layers
from keras.models import Model
try: [tf.config.experimental.set_memory_growth(gpu, True) for gpu in tf.config.experimental.list_physical_devices("GPU")]

except: pass

class HTR_Model:

    def __init__(self, img_shape, characters_num, vocab):
        self.img_shape = img_shape
        self.characters_num = characters_num
        self.vocab = vocab
        self.model = self.build_model()

    def build_model(self, activation="leaky_relu", dropout=0.2):
        data = layers.Input(name='input', shape=self.img_shape)
        data_norm = layers.Lambda(lambda x: x / 255)(data)

        res_block1 = residual_block(data_norm, 32, activation=activation, skip_conv=True, strides=1, dropout=dropout)
        res_block1 = residual_block(res_block1, 32, activation=activation, skip_conv=True, strides=2, dropout=dropout)
        res_block1 = residual_block(res_block1, 32, activation=activation, skip_conv=False, strides=1, dropout=dropout)

        res_block2 = residual_block(res_block1, 64, activation=activation, skip_conv=True, strides=2, dropout=dropout)
        res_block2 = residual_block(res_block2, 64, activation=activation, skip_conv=False, strides=1, dropout=dropout)

        res_block3 = residual_block(res_block2, 128, activation=activation, skip_conv=True, strides=2, dropout=dropout)
        res_block3 = residual_block(res_block3, 128, activation=activation, skip_conv=True, strides=1, dropout=dropout)
        res_block3 = residual_block(res_block3, 128, activation=activation, skip_conv=True, strides=2, dropout=dropout)
        res_block3 = residual_block(res_block3, 128, activation=activation, skip_conv=False, strides=1, dropout=dropout)

        reshape = layers.Reshape((res_block3.shape[-3] * res_block3.shape[-2], res_block3.shape[-1]))(res_block3)

        LSTM1 = layers.Bidirectional(layers.LSTM(256, return_sequences=True))(reshape)
        LSTM1 = layers.Dropout(dropout)(LSTM1)

        LSTM2 = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(LSTM1)
        LSTM2 = layers.Dropout(dropout)(LSTM2)

        output = layers.Dense(self.characters_num + 1, activation="softmax", name="output")(LSTM2)

        model = Model(inputs=data, outputs=output)

        return model

    def compile_model(self):
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
        self.model.compile(loss=CTCloss(), optimizer=optimizer, metrics=[CERMetric(vocabulary=self.vocab), WERMetric(vocabulary=self.vocab)], run_eagerly=False)

    def train(self, train, validate, epochs, workers, callbacks):
        self.model.fit(train, validation_data=validate, epochs=epochs, workers=workers, callbacks=callbacks)

    def validate(self, validate):
        return self.model.evaluate(validate)

    def predict(self, x_test):
        return self.model.predict(x_test)

    def summary(self, line_length):
        return self.model.summary(line_length=line_length)

