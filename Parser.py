import streamlit as st
import re
import os
import json

from loader import make_sentence_pairs
from audio_handler import make_bilingual_mp3, make_audio_byte

# -------------------------------------------------
# Streamlit Settings
# -------------------------------------------------
st.set_page_config(page_title="Text Processor", layout="wide")

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "pairs" not in st.session_state:
    st.session_state.pairs = None

if "audio_cache" not in st.session_state:
    st.session_state.audio_cache = {}

# -------------------------------------------------
# Save Progress Helpers
# -------------------------------------------------
PROGRESS_FILE = "reading_progress.json"


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=4)


# Load existing save state
progress_state = load_progress()


# -------------------------------------------------
# Helper: Audio with cache
# -------------------------------------------------
def play_tts(text, lang="de"):
    key = (lang, text)

    if key not in st.session_state.audio_cache:
        st.session_state.audio_cache[key] = make_audio_byte(text, lang)

    st.audio(st.session_state.audio_cache[key], format="audio/mp3")


# -------------------------------------------------
# Helper: Chapter splitting
# -------------------------------------------------
def split_into_sentences_german(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def load_text_files(folder="textFiles"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return [f for f in os.listdir(folder) if f.endswith(".txt")]


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------------------------
# Processing text (your original function)
# -------------------------------------------------
def process_the_text(text):
    cleaned = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)

    pairs = make_sentence_pairs(cleaned)
    st.session_state.pairs = pairs

    st.subheader("German – English sentence pairs")

    for i, pair in enumerate(pairs, 1):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"**🇩🇪 German {i}**")
            st.write(pair["german"])

        with col2:
            st.markdown(f"**🇬🇧 English {i}** by {pair['provider']}")
            st.write(pair["english"])

        with col3:
            play_tts(pair["german"], "de")
            play_tts(pair["english"], "en")

        st.divider()


def bilingual_audio(text):
    cleaned = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned)

    pairs = make_sentence_pairs(cleaned)
    make_bilingual_mp3(pairs)


# -------------------------------------------------
#  🔥 NEW SECTION: Book Selector + Chapter Selection + Auto-Save Progress
# -------------------------------------------------
st.header("📚 Select Files and Chapters")

book_files = load_text_files("textFiles")

if book_files:

    # Use columns to make UI narrower
    colBook, _ = st.columns([1, 1])   # book selector is half-width
    colSelect, _ = st.columns([1, 1]) # chapter selector is half-width
    colA, colB = st.columns(2)        # buttons

    with colBook:
        selected_book = st.selectbox("Select a book:", book_files)

    # Load full German text
    full_path = os.path.join("textFiles", selected_book)
    book_text = load_text(full_path)

    # Split into 10-sentence chapters
    sentences = split_into_sentences_german(book_text)
    chapter_size = 10
    num_chapters = (len(sentences) + chapter_size - 1) // chapter_size

    st.write(f"**This book contains {num_chapters} chapters** (10 sentences each).")

    # Load saved chapters if available
    saved_chapters = progress_state.get(selected_book, [])

    with colSelect:
        selected_chapters = st.multiselect(
            "Choose chapters to load into processor:",
            list(range(1, num_chapters + 1)),
            default=saved_chapters
        )

    # Build combined chapter text
    combined_text = ""
    for ch in selected_chapters:
        start = (ch - 1) * chapter_size
        end = min(ch * chapter_size, len(sentences))
        combined_text += " ".join(sentences[start:end]) + "\n"

    # ✅ Load + Auto Save Progress

    colA, colB = st.columns(2)

    with colA:
        if st.button("➡ Load selected chapters into Text Processor"):
            st.session_state.input_text = combined_text

            # ✅ Automatically save progress
            progress_state[selected_book] = selected_chapters
            save_progress(progress_state)

            # Store a flag to show success in colB
            st.session_state.load_success = True
        else:
            st.session_state.load_success = False

    # ✅ Display success message next to button
    with colB:
        if st.session_state.get("load_success"):
            st.success("Chapters loaded and progress auto-saved!")


else:
    st.info("No .txt files found in /textFiles. Add files to enable chapter selection.")


# -------------------------------------------------
#   ORIGINAL TEXT PROCESSOR UI
# -------------------------------------------------
st.header("📝 Text Processor (German → English)")

text_col1, text_col2 = st.columns(2)
with text_col1:
    st.write("Paste text manually or load chapters from the reader above.")

with text_col2:
    if st.button("Remove text"):
        st.session_state.input_text = ""
        user_text = ""

# Main input box
user_text = st.text_area(
    "hidden_label",
    value=st.session_state.input_text,
    label_visibility="collapsed",
    height=300,
    placeholder="Paste a large German text here…"
)

st.session_state.input_text = user_text

# Submit
if st.button("Submit"):
    if user_text.strip():
        process_the_text(user_text)
    else:
        st.warning("Please enter text before submitting.")

# Bilingual audio
if st.button("Bilingual audio"):
    if user_text.strip():
        bilingual_audio(user_text)
    else:
        st.warning("Please enter text before submitting.")