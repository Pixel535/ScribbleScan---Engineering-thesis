import typing

import numpy as np
from mltu.inferenceModel import OnnxInferenceModel
from mltu.transformers import ImageResizer
from mltu.utils.text_utils import ctc_decoder

class ReadImages(OnnxInferenceModel):

    def __init__(self, vocab: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vocab = vocab

    def predict(self, data: np.ndarray):
        data = ImageResizer.resize_maintaining_aspect_ratio(data, *self.input_shape[:2][::-1])
        data_pred = np.expand_dims(data, axis=0).astype(np.float32)
        prediction = self.model.run(None, {self.input_name: data_pred})[0]
        text = ctc_decoder(prediction, self.vocab)[0]
        return text

