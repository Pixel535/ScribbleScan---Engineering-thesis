import tensorflow as tf
from mltu.losses import CTCloss
from mltu.metrics import CERMetric, WERMetric
from mltu.model_utils import activation_layer
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

    def convolutional_block(self, x, filter_num, how_many_layers, dropout, strides_iteration_change, activation):

        for i in range(how_many_layers):
            strides = 1
            if i in strides_iteration_change:
                strides = 2
            # Convolutional Layer 1
            x = layers.Conv2D(filter_num, (5, 5), padding="same", strides=strides, kernel_initializer='he_uniform')(x)
            x = layers.BatchNormalization()(x)

            # Convolutional Layer 2
            x = layers.Conv2D(filter_num, (3, 3), padding="same", kernel_initializer='he_uniform')(x)
            x = layers.BatchNormalization()(x)

            x = layers.Add()([x, x])
            x = activation_layer(x, activation=activation)
            x = layers.Dropout(dropout)(x)

        return x

    def dense_block(self, x, neuron_num, activation, dropout):

        x = layers.Dense(neuron_num)(x)
        x = activation_layer(x, activation=activation)
        x = layers.Dropout(dropout)(x)

        return x

    def build_model(self, activation="leaky_relu", dropout=0.1):
        data = layers.Input(name='input', shape=self.img_shape)
        data_norm = layers.Lambda(lambda x: x / 255)(data)

        # Convolutional Blocks
        conv_block1 = self.convolutional_block(data_norm, 32, how_many_layers=3, dropout=dropout, strides_iteration_change=[1], activation=activation)
        conv_block2 = self.convolutional_block(conv_block1, 64, how_many_layers=2, dropout=dropout, strides_iteration_change=[0], activation=activation)
        conv_block3 = self.convolutional_block(conv_block2, 128, how_many_layers=4, dropout=dropout, strides_iteration_change=[0, 2], activation=activation)
        conv_block4 = self.convolutional_block(conv_block3, 256, how_many_layers=1, dropout=dropout, strides_iteration_change=[2], activation=activation)

        # Reshaping
        reshape = layers.Reshape((conv_block4.shape[-3] * conv_block4.shape[-2], conv_block4.shape[-1]))(conv_block4)
        dropout_layer = layers.Dropout(dropout)(reshape)

        # Dense Blocks
        dense_block1 = self.dense_block(x=dropout_layer, neuron_num=512, activation=activation, dropout=dropout)
        dense_block2 = self.dense_block(x=dense_block1, neuron_num=256, activation=activation, dropout=dropout)

        output = layers.Dense(self.characters_num + 1, activation="softmax", name="output")(dense_block2)

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

