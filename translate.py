import os
import re
import pytesseract
import cv2
import numpy as np
import deepl
from PIL import Image, ImageEnhance, ImageFilter
from dotenv import load_dotenv


load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path: str) -> str:
    """
    Преобразует изображение, увеличивает его разрешение и сохраняет.

    :param image_path: Путь к исходному изображению.
    :return: Путь к обработанному изображению.
    """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape
    new_width = width * 3
    new_height = height * 3
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    processed_image_path = 'processed_' + image_path
    cv2.imwrite(processed_image_path, resized_image)

    return processed_image_path

def extract_text(image_path: str) -> str:
    """
    Извлекает текст из изображения с помощью Tesseract.

    :param image_path: Путь к изображению.
    :return: Извлечённый текст.
    """
    try:
        processed_image_path = preprocess_image(image_path)
        img = Image.open(processed_image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
        return ""

def translate_text(text: str, dest_language: str = 'ru') -> str:
    """
    Переводит текст с помощью API DeepL.

    :param text: Текст для перевода.
    :param dest_language: Язык перевода (по умолчанию — русский).
    :return: Переведённый текст.
    """
    try:
        translator = deepl.Translator(DEEPL_API_KEY)
        translated_text = translator.translate_text(text, target_lang=dest_language.upper())
        return translated_text.text
    except deepl.DeepLException as e:
        print(f"Ошибка при переводе текста с использованием DeepL API: {e}")
        return ""

def translate_main(image_path: str, dest_language: str = 'ru') -> list:
    """
    Извлекает текст из изображения, очищает его и переводит.

    :param image_path: Путь к изображению.
    :param dest_language: Язык перевода (по умолчанию — русский).
    :return: Список с исходным и переведённым текстом.
    """
    text = extract_text(image_path)
    result_text = []

    if text:
        cleaned = re.sub(r'[^a-zA-Z\s]', '', text)
        cleaned = ' '.join(cleaned.split())
        result_text.append(cleaned)
        translated_text = translate_text(cleaned, dest_language)
        result_text.append(translated_text)
    else:
        print("Не удалось извлечь текст из изображения.")
    
    # Удаление всех файлов изображений в текущей директории
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    for filename in os.listdir('.'):
        if filename.lower().endswith(image_extensions):
            file_path = os.path.join('.', filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    return result_text
