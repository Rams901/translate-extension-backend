from torch import cuda
from transformers import pipeline

# load helsinki models
class transcriptionModel():

    def __init__(self):
        self.model_ar = pipeline("translation", "assets/models/opus-mt-ar-en")
        self.model_fr = pipeline("translation", "assets/models/opus-mt-fr-en")
    
    def translate(self, text, lang):
      if lang == "fr":
        translation = self.model_fr(text)
      else:
        translation = self.model_ar(text)

      cuda.empty_cache()

      return translation[0]['translation_text']
    
model = transcriptionModel()

def get_tr_model():
    return model
