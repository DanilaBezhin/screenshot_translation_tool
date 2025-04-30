# Screenshot Translation Tool

## Description

This project provides a screenshot tool that allows the user to select an area on the screen, capture the screenshot, extract the text from it using OCR (Optical Character Recognition), and then translate the extracted text into a target language using the DeepL API. The tool also features an interactive GUI that displays the original and translated text, with the option to copy the results to the clipboard.

The application is built using Python, leveraging various libraries such as PyQt5 for GUI creation, pytesseract for OCR text extraction, and DeepL for translation.

## Features
- **Screen Capture**: Allows users to select a region of the screen and capture a screenshot.
- **Text Extraction**: Extracts text from the screenshot using Tesseract OCR.
- **Translation**: Translates the extracted text into the target language (default is Russian) using DeepL API.
- **GUI Interface**: Displays both the original and translated text in a user-friendly interface with options to copy the text to the clipboard.
- **Keyboard Shortcuts**: The tool can be triggered using a keyboard shortcut (`Ctrl + Alt + W`).

## Installation

To install the necessary dependencies, create a virtual environment and use `pip` to install the required packages.

1. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # for Windows
    source venv/bin/activate  # for Linux/Mac
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the project directory with the following content (replace with your own DeepL API key):
    ```
    DEEPL_API_KEY=your-api-key-here
    ```

4. **Run the application**:
    To start the application, simply run:
    ```bash
    python main.py
    ```

## Dependencies
The project requires the following libraries:

- `certifi==2025.4.26`
- `charset-normalizer==3.4.1`
- `deepl==1.21.1`
- `idna==3.10`
- `keyboard==0.13.5`
- `numpy==2.2.5`
- `opencv-python==4.11.0.86`
- `packaging==25.0`
- `pillow==11.2.1`
- `pyperclip==1.9.0`
- `PyQt5==5.15.11`
- `PyQt5-Qt5==5.15.2`
- `PyQt5_sip==12.17.0`
- `pytesseract==0.3.13`
- `python-dotenv==1.1.0`
- `requests==2.32.3`
- `urllib3==2.4.0`

## Usage

1. Run the application.
2. Press the keyboard shortcut `Ctrl + Alt + W` to start capturing a screenshot.
3. Select the area on the screen you want to capture.
4. After the screenshot is captured, the tool will extract the text from the image and translate it.
5. The translated text will be displayed in a GUI window, with an option to copy the original or translated text to the clipboard.

