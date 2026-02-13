import streamlit as st
import os
import re

FOLDER_PATH = "textFiles"

st.title("📄 Text File Viewer")

# --------- Encoding-Safe Loader ---------
def read_text_file_safely(path):
    encodings = [
        "utf-8", "utf-8-sig",
        "utf-16", "utf-16-le", "utf-16-be",
        "cp1252", "latin-1",
    ]
    last_error = None
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read(), enc, None
        except Exception as e:
            last_error = e

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), "utf-8 (errors=replace)", None
    except Exception as e:
        return None, None, f"Failed to read file. Last error: {last_error or e}"


# --------- Text Formatting: Insert blank line after every 10 sentences ---------
def format_text_every_10_sentences(text):
    # Split into sentences using basic punctuation detection
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    formatted = []

    for i, sentence in enumerate(sentences, start=1):
        formatted.append(sentence)
        if i % 10 == 0:
            formatted.append("")  # empty line
            formatted.append(f"{i}")  # empty line
            formatted.append("")  # empty line

    return "\n".join(formatted)


# --------- UI ---------
if not os.path.exists(FOLDER_PATH):
    st.error(f"Folder not found: {FOLDER_PATH}")
else:
    files = [f for f in os.listdir(FOLDER_PATH) if f.lower().endswith(".txt")]
    files.sort(key=str.lower)

    if not files:
        st.warning("No text files found.")
    else:
        selected_file = st.selectbox("Choose a file:", files)

        if selected_file:
            file_path = os.path.join(FOLDER_PATH, selected_file)
            content, encoding_used, err = read_text_file_safely(file_path)

            if err:
                st.error(err)
            else:
                formatted = format_text_every_10_sentences(content)

                st.caption(f"Encoding used: **{encoding_used}**")
                st.text_area("Content (formatted)", formatted, height=800)