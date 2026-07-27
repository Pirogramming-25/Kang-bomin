import cv2
from paddleocr import PaddleOCR

_ocr_instance = None

def get_ocr():
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(
            use_textline_orientation=True,
            lang='korean',
            enable_mkldnn=False,
        )
    return _ocr_instance


def _ocr_on_image(img):
    ocr = get_ocr()
    result = ocr.predict(img)
    lines = []
    for page in result:
        lines.extend(page.get('rec_texts', []))
    return lines


def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    calorie_region = img[0:int(h * 0.4), int(w * 0.45):w]
    calorie_region = cv2.resize(calorie_region, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    calorie_lines = _ocr_on_image(calorie_region)

    table_region = img[int(h * 0.35):h, 0:w]
    table_lines = _ocr_on_image(table_region)

    return calorie_lines + table_lines