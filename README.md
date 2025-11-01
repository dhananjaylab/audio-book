# 🎧 DhananjayLab AudioBook Generator

This project is a web application built with **Streamlit** that converts popular e-book formats (PDF, DOCX, EPUB, TXT) into a downloadable or playable audiobook using the **Google Text-to-Speech (gTTS)** engine.

It allows users to turn their documents and novels into an accessible, hands-free listening experience.

## ✨ Features

* **Multi-Format Support:** Converts PDF, DOCX, EPUB, and TXT files.
* **Language Selection:** Supports multiple languages for text-to-speech conversion (based on gTTS capabilities).
* **Real-time Feedback:** Shows a loading spinner during the text extraction and audio generation process.
* **Robust Parsing:** Includes error handling for better stability with non-standard files.

## 🛠️ Setup and Installation

### Prerequisites

You need **Python 3.8+** installed on your system.

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/dhananjaylab/audio-book.git](https://github.com/dhananjaylab/audio-book.git)
    cd dhananjaylab-audio-book
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run audio_book.py
    ```
    The application will automatically open in your default web browser.

## 📖 How to Use

1.  Open the Streamlit app in your browser.
2.  Select your desired **Output Language** from the dropdown menu.
3.  Click the "Browse files" button and upload your **PDF, DOCX, TXT, or EPUB** file.
4.  Wait for the progress spinner to disappear.
5.  The audio player will appear, allowing you to listen to your audiobook.
6.  You can also use the three-dot menu on the audio player to download the `.mp3` file.

## 🧑‍💻 Code Structure

| File | Description |
| :--- | :--- |
| `audio_book.py` | Contains the Streamlit app definition, text extraction logic, and TTS conversion. |
| `requirements.txt` | Lists all necessary Python packages (streamlit, gtts, pdfplumber, etc.). |