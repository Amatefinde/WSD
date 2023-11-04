import easyocr
import cv2
import time
from random import randint
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import numpy as np
BATCH = 50
reader = easyocr.Reader(['en'], recognizer=False)

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed").to("cuda")


def detect_words(img):
    start_time = time.time()

    result = reader.detect(img, width_ths=0, slope_ths=0.2, text_threshold=0, height_ths=0.0)
    crops = []
    for i in result[0][0]:

        # img = cv2.rectangle(img, (i[0], i[2]), (i[1], i[3]),
        #                       (randint(100, 200), randint(100, 200), randint(100, 200)), 1)
        obj = {  # i[0] - start; i[2] - top; i[1] - end; i[3] - bottom;
            "start": i[0],
            "end": i[1],
            "top": i[2],
            "bottom": i[3],
            "image": img[i[2]:i[3], i[0]:i[1]],
        }
        # img = cv2.drawMarker(img, (i[1], i[3]), (255, 0, 255))

        # cv2.imshow("", img)
        # cv2.waitKey()

        crops.append(obj)

    print("Word detection: ", time.time() - start_time, "sec")
    start_time = time.time()


    images_for_detection = [cv2.copyMakeBorder(x["image"], 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255)) for x in crops]

    generated_text = []
    for i in range(0, len(images_for_detection), BATCH):
        elements = images_for_detection[i: i + BATCH]
        pixel_values = processor(elements, return_tensors="pt").pixel_values.to("cuda")
        generated_ids = model.generate(pixel_values).to("cpu")
        batch_generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)
        generated_text.extend(batch_generated_text)
    for idx, obj in enumerate(crops):
        del obj["image"]
        obj["text"] = generated_text[idx]
    print("Word recognition: ", time.time() - start_time, "sec")
    return crops


if __name__ == "__main__":
    path_img = "test_content/img.png"
    image = cv2.imread(path_img)
    crop_images = detect_words(image)
    crop_images = detect_words(image)
    crop_images = detect_words(image)


