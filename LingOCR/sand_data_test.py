import json
import cv2
import requests
import time
import numpy as np

image = cv2.imread("img.png")


def call_to_ocr(img, url='http://192.168.31.23:8007/parse_image'):
    _, img_encoded = cv2.imencode(".png", img)
    files = {"file": ("image.png", img_encoded.tobytes())}
    response = requests.post(url, files=files)


call_to_ocr(image)




