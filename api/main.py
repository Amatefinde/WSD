from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
from LingOCR import LingDetection
import wsd as wsd
from api.schemas import BaseInput
import numpy as np
import cv2


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4444",
    "http://192.168.31.23:4444",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_meaning")
def get_meaning(input_word: BaseInput):
    return wsd.get_current_word_meaning(input_word.word, input_word.context, input_word.meanings)


@app.post("/parse_image")
async def create_upload_file(file: UploadFile) -> list:
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    print("Попали в эндпоинт для парсинга картинок")
    return LingDetection.detect_words(image)