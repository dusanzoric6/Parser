import streamlit as st
import os

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
                st.caption(f"Encoding used: **{encoding_used}**")
                st.text_area("Content", content, height=600)