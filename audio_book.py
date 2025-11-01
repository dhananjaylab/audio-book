# dhananjaylab-audio-book/audio_book.py

# import the required modules
import streamlit as st
from gtts import gTTS, lang
import pdfplumber
from docx import Document 
from ebooklib import epub
from ebooklib.epub import read_epub
import tempfile
import os
import re

# --- Configuration and Setup ---
st.set_page_config(page_title="Streamlit AudioBook App", layout="centered")

st.title("🎧 Streamlit AudioBook Generator")
st.info("Convert your E-book (PDF, TXT, DOCX, EPUB) to a spoken audiobook.")

# Get supported languages from gTTS
SUPPORTED_LANGUAGES = lang.tts_langs()
# Filter for common languages for cleaner UI
COMMON_LANGS = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 'hi': 'Hindi'}
LANG_OPTIONS = {name: code for code, name in SUPPORTED_LANGUAGES.items() if code in COMMON_LANGS}
# Add default choice to the beginning of the dictionary
LANG_OPTIONS = {"English": "en", **LANG_OPTIONS}

# Voice Character/Accent Options (using different Google TLDs)
VOICE_OPTIONS = {
    "US English (Standard)": "com",
    "UK English (Accent)": "co.uk",
    "Australian English (Accent)": "com.au",
    "Indian English (Accent)": "co.in",
    "French (Accent)": "fr",
    "Spanish (Accent)": "es"
}

# --- Widgets for User Configuration (Sidebar) ---
st.sidebar.header("Configuration")

# Language Selection
selected_lang = st.sidebar.selectbox(
    "Select Output Language:",
    options=list(LANG_OPTIONS.keys()),
    format_func=lambda x: f"{x} ({LANG_OPTIONS[x]})"
)
lang_code = LANG_OPTIONS[selected_lang]

# Voice Selection
st.sidebar.header("Voice Settings")
selected_voice_name = st.sidebar.selectbox(
    "Select Voice/Accent:",
    options=list(VOICE_OPTIONS.keys()),
    help="Different hosts (TLDs) can provide distinct accents or voices."
)
voice_tld = VOICE_OPTIONS[selected_voice_name]

# File Uploader
book = st.file_uploader(
    "Please upload your file", 
    type=['pdf', 'txt', 'docx', 'epub'],
    help="Supported formats: PDF, Plain Text, Word Document, EPUB."
)


# --- Text Extraction Functions (Cached for performance) ---

@st.cache_data(show_spinner="Extracting text from DOCX file...")
def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    try:
        doc = Document(file)
        full_text = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(full_text)
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return ""

@st.cache_data(show_spinner="Extracting text from EPUB file...")
def extract_text_from_epub(file):
    """Extracts and cleans text from an EPUB file."""
    tmp_file_path = None
    try:
        # Save uploaded file to a temporary location for epub reader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        book = read_epub(tmp_file_path)
        chapters = []
        for item in book.get_items():
            # Check if item is a document type
            if item.get_type() == 9: # 9 is the numerical value for ebooklib.ITEM_DOCUMENT
                # Decode content and remove common HTML tags
                content = item.get_content().decode('utf-8', 'ignore')
                cleaned_content = re.sub('<[^<]+?>', '', content)
                chapters.append(cleaned_content)
                
        return "\n".join(chapters)
    except Exception as e:
        st.error(f"Error extracting text from EPUB. Ensure it's a valid format. Error: {e}")
        return ""
    finally:
        # Clean up temp file
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)


# --- Main Logic: File Upload and Conversion ---
all_text = ""

if book:
    with st.spinner(f"Parsing {book.name}... Please wait."):
        if book.type == "application/pdf":
            try:
                all_text = ""
                with pdfplumber.open(book) as pdf:
                    for page in pdf.pages:
                        single_page_text = page.extract_text()
                        if single_page_text:
                            all_text += '\n' + single_page_text
            except Exception as e:
                st.error(f"Error processing PDF file. Is it secured or corrupt? Error: {e}")
                
        elif book.type == "text/plain":
            try:
                all_text = book.read().decode("UTF-8")
            except Exception as e:
                st.error(f"Error reading TXT file: {e}")
                
        elif book.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            all_text = extract_text_from_docx(book)
            
        elif book.type == "application/epub+zip":
            all_text = extract_text_from_epub(book)
            
        else:
            st.warning(f"Unsupported file type: {book.type}")

# Check if there is text to convert
if all_text:
    # Remove excessive whitespace that can confuse gTTS
    cleaned_text = ' '.join(all_text.split())
    
    if len(cleaned_text) > 0:
        with st.spinner(f"Converting text to audio ({selected_lang}, {selected_voice_name})..."):
            tmp_audio_path = None
            try:
                # Use a temporary file to save the MP3
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                    tts = gTTS(
                        text=cleaned_text, 
                        lang=lang_code, 
                        tld=voice_tld  # Pass the selected TLD here
                    )
                    tts.write_to_fp(tmp_audio)
                    tmp_audio_path = tmp_audio.name
                
                # Open and read the content of the file
                with open(tmp_audio_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()

                # Create an audio player widget
                st.subheader("Your Audiobook is Ready! 🔊")
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                
            except Exception as e:
                st.error(f"Text-to-Speech (gTTS) conversion failed. This might be due to an unsupported language/text combination. Error: {e}")
                
            finally:
                # Clean up the temporary audio file
                if tmp_audio_path and os.path.exists(tmp_audio_path):
                    os.remove(tmp_audio_path)
                
    else:
        st.warning("Extracted text was empty or contained only non-printable characters.")

elif book is not None:
    st.warning("No text could be extracted from the uploaded file.")