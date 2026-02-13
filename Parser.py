import streamlit as st
from loader import make_sentence_pairs
from audio_handler import make_audio_byte

st.set_page_config(page_title="Text Processor", layout="wide")

# ---------------------------------------------
# Initialize session state variables
# ---------------------------------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "pairs" not in st.session_state:
    st.session_state.pairs = None

if "audio_cache" not in st.session_state:
    st.session_state.audio_cache = {}   # key: (lang, text), value: bytes


# ---------------------------------------------
# Audio helper with caching
# ---------------------------------------------
def play_tts(text, lang="de"):
    key = (lang, text)

    # Use cached audio if available
    if key not in st.session_state.audio_cache:
        st.session_state.audio_cache[key] = make_audio_byte(text, lang)

    st.audio(st.session_state.audio_cache[key], format="audio/mp3")


# ---------------------------------------------
# Processing text
# ---------------------------------------------
def process_the_text(text):
    pairs = make_sentence_pairs(text)
    st.session_state.pairs = pairs  # store in memory

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


# ---------------------------------------------
# UI
# ---------------------------------------------
st.title("Text Processor")
text_col1, text_col2 = st.columns(2)
with text_col1:
    st.write("Enter your text below or open the **Text Reader** page from the sidebar.")
with text_col2:
    # Remove text button
    if st.button("Remove text"):
        st.session_state.input_text = ""
        user_text = ""

# Load previously entered text
user_text = st.text_area(
    "hidden_label",
    value=st.session_state.input_text,
    label_visibility="collapsed",
    height=300,
    placeholder="Paste a large German text here..."
)

# Store text immediately when typed
st.session_state.input_text = user_text

# Submit button
if st.button("Submit"):
    if user_text.strip():
        process_the_text(user_text)
    else:
        st.warning("Please enter some text before submitting.")

# If pairs already exist, show them immediately
elif st.session_state.pairs:
    process_the_text(st.session_state.input_text)