import json
import cv2
import pdfplumber
import io
import numpy as np
from typing import TypedDict, List
import time
import requests


def call_to_ocr(np_image, url='http://192.168.31.23:8007/parse_image'):
    image_json = json.dumps({"image_data": np_image.tolist()})
    response = requests.post(url, data=image_json, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()


class WordSchema(TypedDict):
    text: str
    start: int
    end: int
    top: int
    bottom: int


class PageSchema(TypedDict):
    pageWidth: int
    pageHeight: int
    words: List[WordSchema]


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 3

SCALE = 6


def parse_pfd(pdf_bytesio: io.BytesIO | str,  static_path: str, literature_number: str | int, use_ocr=False) -> List[PageSchema]:
    parsed_pages = []
    literature_number = str(literature_number)
    with pdfplumber.open(pdf_bytesio) as pdf:
        for page in pdf.pages:
            print(f"Pages: {page.page_number}")

            parsed_page = {
                "pageWidth": int(page.bbox[2]),
                "pageHeight": int(page.bbox[3]),
                "words": [],
            }
            image = page.to_image(width=parsed_page["pageWidth"]*SCALE)

            cv2_image = np.array(image.original)
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)

            if use_ocr:
                parsed_page["words"] = call_to_ocr(cv2_image)

            else:
                for element in page.extract_words():
                    parsed_page["words"].append({
                        "text": element["text"],
                        "start": int(element["x0"]) * SCALE,
                        "end": int(element["x1"]) * SCALE,
                        "top": int(element["top"]) * SCALE,
                        "bottom": int(element["bottom"]) * SCALE,
                    })

            # for word in parsed_page["words"]:
            #     cv2_image = cv2.rectangle(cv2_image, (word["start"], word["top"]), (word["end"], word["bottom"]), (255, 0, 0), 2)
            #     cv2_image = cv2.putText(cv2_image, word["text"], (word["start"], word["bottom"]), font, fontScale, (0, 0, 200), 5, cv2.LINE_AA)
            # cv2_image = cv2.resize(cv2_image, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
            add_later = "." if static_path[0] in "/\\" else ""
            fullpath = add_later + static_path + "/" + literature_number + "_" + str(page.page_number) + ".png"
            image.save(fullpath)
            parsed_pages.append(parsed_page)
        return parsed_pages


if __name__ == "__main__":
    time_total = time.time()
    pdf_file_path = 'Naruto v01.pdf'
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_example = io.BytesIO(pdf_file.read())
    result = parse_pfd(pdf_example, "/testStatic", literature_number=1, use_ocr=True)
    print(result)
    print(time.time()-time_total)
