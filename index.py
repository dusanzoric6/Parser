import streamlit as st
from loader import make_sentence_pairs
from audio_handler import make_audio_byte


st.set_page_config(layout="wide")


def play_tts(text, lang="de"):
    audio_bytes = make_audio_byte(text, lang)
    st.audio(audio_bytes, format="audio/mp3")

def process_the_text(text):
    """
    Called when the user clicks Submit
    """
    pairs = make_sentence_pairs(text)

    st.subheader("German – English sentence pairs")

    for i, pair in enumerate(pairs, 1):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**🇩🇪 German {i}**")
            st.write(pair["german"])
        with col2:
            st.markdown(f"**🇬🇧 English {i}**")
            st.write(pair["english"])
        with col3:
            play_tts(pair["german"], "de")
            play_tts(pair["english"], "en")

        st.divider()

# ---- UI ----
st.title("Text Processor")

st.write("Enter your text below:")

# Big text box
user_text = st.text_area(
"hidden_label",
    label_visibility="collapsed",
    height=300,
    placeholder="Paste a large German text here..."
)

# Submit button
if st.button("Submit"):
    if user_text.strip():
        process_the_text(user_text)
    else:
        st.warning("Please enter some text before submitting.")
