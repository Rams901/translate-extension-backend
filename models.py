import whisper
from fastapi import FastAPI, File, UploadFile
import shutil
# import pycld2 as cld2
# from langdetect import detect
import langid

# model = whisper.load_model("models/small.pt",)

from torch import cuda 
def bytes_to_file(file):
    with open(file.filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file.filename
class whisperModel():

    def __init__(self):
        self.model = whisper.load_model("assets/models/whisper_small.pt",)

    def transcribe(self, path):
        print(path)
        transcription = self.model.transcribe(path)
        # for now just take the text from each segment and language
        transcript, language = transcription['text'], transcription['language']
        cuda.empty_cache()
        return transcript, language
    
model = whisperModel()

def get_model():
    return model

def detect_language(input_text):
    if not input_text:
        return "unknown"
    details = langid.classify(input_text)
    detected_langauge = details[0]
    # if detected_langauge == "unknown":
    #     language_code = detect(input_text)
    #     return language_code
    # else:
    return detected_langauge
