# Fastapi
# endpoint for transcription, accepts a bytes-like file
# endpoint for translation
# make sure to store everything in db
# fastapi has sqlite?
# Import key libraries and packages

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import pickle
import uvicorn
import pandas as pd

import os
import sys
from fastapi.middleware.cors import CORSMiddleware

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler

from models import *
from fastapi.responses import StreamingResponse, ORJSONResponse

from pydantic import BaseModel

import asyncio
import os
from typing import AsyncIterable, Awaitable
import time
from translate import *
from firebase_store import *
import ast
from pydantic import BaseModel

# Templates configuration
# API base configuration
app = FastAPI(default_response_class=ORJSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_name = bytes_to_file(file)
    return {"filename": file_name}

@app.get('/')
async def retrieve_docs(fr_store: firebaseStore = Depends(get_fr_store)):
    documents = fr_store.read_all_document()
    return documents

@app.post("/transcribe/")
async def process_input(text: str, file: UploadFile = File(default=None), model: whisperModel = Depends(get_model)):
    
    if file:
        file_name = bytes_to_file(file)
        # delete after transcription is done
        transcription, lang = model.transcribe(file_name)
        os.remove(file_name)
        # store the transcription along with the file somewhere
        # will probs start with google firebase

        return {"transcription": transcription, "language": lang}
    # detect language
    lang = detect_language(text)
    return {"input text": text, "language": lang}
 
@app.post('/translate/')
async def translate_input(text: str, file: UploadFile = File(default=None), whisper_model: whisperModel = Depends(get_model), tr_model: transcriptionModel = Depends(get_tr_model), fr_store: firebaseStore = Depends(get_fr_store)):
    if file:
        file_name = bytes_to_file(file)
        # delete after transcription is done
        transcription, lang = whisper_model.transcribe(file_name)
        os.remove(file_name)
        # store the transcription along with the file somewhere
        # will probs start with google firebase

        mp = {"transcription": transcription, "language": lang}
    else:
        # detect language
        lang = detect_language(text)
        mp = {"input text": text, "language": lang}
    text, lang = mp.values()

    translation = tr_model.translate(text, lang)
    
    mp['translation'] = translation

    # Store everything transcription/text, lang and 
    fr_store.create_document(mp)

    return mp


if __name__=='__main__':
    uvicorn.run('main:app', reload=True)