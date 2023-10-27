from fastapi import FastAPI
import wsd as wsd
from wsdAPI.schemas import BaseInput

app = FastAPI()


@app.post("/get_meaning")
def get_meaning(input_word: BaseInput):
    return wsd.get_current_word_meaning(input_word.word, input_word.context, input_word.meanings)


