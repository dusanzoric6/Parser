# app.py
import os
import io
import streamlit as st

# --- Translators ---
import deepl
from googletrans import Translator  # googletrans==4.0.0-rc1 recommended

# --- TTS (Text-to-Speech) ---
from gtts import gTTS  # simple, cloud-based

# -------------- Page Setup --------------
st.set_page_config(
    page_title="DE ➜ EN Translate + Audio",
    page_icon="🎧",
    layout="wide",
)

st.markdown(
    """
    <style>
    .kicker {font-size:0.8rem; color:#666; text-transform: uppercase; letter-spacing:.04em; margin-bottom: 0.25rem;}
    .box {padding: 1rem; border: 1px solid #e8e8e8; border-radius: 10px; background-color: #fbfbfb;}
    .muted {color: #666; font-size: 0.85rem;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🇩🇪 ➜ 🇬🇧 Translate to English + Generate Audio")
st.caption("Uses DeepL with Google Translate as a fallback. Generates MP3 audio for German and English.")

# -------------- Configuration / Translators --------------
@st.cache_resource(show_spinner=False)
def get_translators():
    # Prefer environment variable
    deepl_api_key = os.getenv("DEEPL_API_KEY", "").strip()

    deepl_trans = None
    if deepl_api_key:
        try:
            deepl_trans = deepl.Translator(deepl_api_key)
        except Exception as e:
            # We'll handle fallback inside safe_translate
            print("DeepL init failed:", e)

    google_trans = Translator()
    return deepl_trans, google_trans

deepl_translator, google_translator = get_translators()

def safe_translate(text, source="DE", target="EN-GB"):
    """
    Try DeepL first. If it fails (invalid token, quota exceeded, etc.)
    fall back to Google Translate.
    Returns: (translated_text or None, engine_name_str)
    """
    # --- Try DeepL ---
    if deepl_translator:
        try:
            result = deepl_translator.translate_text(
                text,
                source_lang=source,
                target_lang=target
            )
            return result.text, "deepl"
        except Exception as e:
            print("DeepL failed → switching to Google Translate:", str(e))

    # --- Fall back to Google ---
    try:
        # googletrans expects lowercase ISO codes (e.g., 'de', 'en')
        g = google_translator.translate(text, src=source.lower(), dest=target.split('-')[0].lower())
        return g.text, "google"
    except Exception as e:
        print("Google Translate also failed:", str(e))
        return None, "failed"

def synthesize_gtts(text: str, lang: str = "en", tld: str | None = None, slow: bool = False) -> bytes:
    """
    Generate MP3 bytes with gTTS. Optionally set tld='co.uk' for a British accent flavor in English.
    """
    if not text or not text.strip():
        return b""
    buf = io.BytesIO()
    if tld:
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
    else:
        tts = gTTS(text=text, lang=lang, slow=slow)
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

# -------------- Sidebar (Options) --------------
with st.sidebar:
    st.header("Options")
    st.write("Default: German → English (UK).")
    source_lang = st.selectbox("Source language", options=["DE"], index=0, help="Fixed to German, as requested.")
    target_lang = "EN-GB"
    british_accent = st.checkbox("Use British English accent (gTTS via tld=co.uk)", value=True)
    slow_speech = st.checkbox("Slow speech", value=False)

    st.divider()
    if os.getenv("DEEPL_API_KEY"):
        st.success("DeepL API key found in environment ✅")
    else:
        st.info("No DeepL API key in environment. App will fall back to Google Translate.")

# -------------- Main UI --------------
st.subheader("Enter German text")
user_text = st.text_area(
    "Paste or type German text here",
    height=200,
    placeholder="Geben Sie hier Ihren deutschen Text ein …",
    label_visibility="collapsed"
)

col_action, col_info = st.columns([1, 3])
with col_action:
    run = st.button("Translate & Generate Audio", type="primary", use_container_width=True)
with col_info:
    st.write("")

if run:
    if not user_text or not user_text.strip():
        st.warning("Please enter some German text first.")
        st.stop()

    with st.spinner("Translating…"):
        translated, engine = safe_translate(user_text.strip(), source=source_lang, target=target_lang)

    if not translated:
        st.error("Translation failed with both DeepL and Google Translate. Please try again later.")
        st.stop()

    # Display results side-by-side, nicely
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="kicker">Original (DE)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box">{user_text.strip().replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Audio (German)</div>', unsafe_allow_html=True)

        # try:
        #     de_audio = synthesize_gtts(user_text.strip(), lang="de", slow=slow_speech)
        #     if de_audio:
        #         st.audio(de_audio, format="audio/mp3")
        #         st.download_button("Download German MP3", data=de_audio, file_name="original_de.mp3", mime="audio/mpeg")
        #     else:
        #         st.info("No audio generated for German text.")
        # except Exception as e:
        #     st.error(f"German TTS failed: {e}")

    with right:
        st.markdown('<div class="kicker">Translated (EN-GB)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box">{translated.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
        st.caption(f"Engine: {'DeepL' if engine=='deepl' else 'Google Translate' if engine=='google' else 'Unknown'}")

        st.markdown('<div class="muted">Audio (English)</div>', unsafe_allow_html=True)
        try:
            tld = "co.uk" if british_accent else None
            en_audio = synthesize_gtts(translated, lang="en", tld=tld, slow=slow_speech)
            if en_audio:
                st.audio(en_audio, format="audio/mp3")
                st.download_button("Download English MP3", data=en_audio, file_name="translated_en.mp3", mime="audio/mpeg")
            else:
                st.info("No audio generated for English text.")
        except Exception as e:
            st.error(f"English TTS failed: {e}")

    st.success("Done ✅")

