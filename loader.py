import deepl
import nltk
import asyncio
from nltk.tokenize import sent_tokenize
from googletrans import Translator
from audio_handler import make_bilingual_mp3, make_audio_byte

# Run once (or keep, it will not re-download)


DEEPL_API_KEY = "0de8b866-1e19-4e03-be74-88f457d89ccd:fx"

deepl_translator = deepl.Translator(DEEPL_API_KEY)
google_translator = Translator()

def safe_translate(text, source="DE", target="EN-GB"):
    """
    Try DeepL first. If it fails (invalid token, quota exceeded, etc.)
    fall back to Google Translate.
    """
    # --- Try DeepL ---
    try:
        result = deepl_translator.translate_text(
            text,
            source_lang=source,
            target_lang=target
        )
        return result.text, "deepl"

    except Exception as e:
        # Detect DeepL key/limit / auth errors
        print("DeepL failed → switching to Google Translate:", str(e))

    # --- Fall back to Google ---
    try:
        g = google_translator.translate(text, src=source.lower(), dest=target.lower())
        return g.text, "google"

    except Exception as e:
        print("Google Translate also failed:", str(e))
        return None, "failed"


def make_sentence_pairs(original_text):
    async def _async_impl():
        nltk.download("punkt")
        nltk.download("punkt_tab")
        german_sentences = sent_tokenize(original_text, language="german")
        pairs = []

        for de in german_sentences:
            result, provider = safe_translate(de,source="DE",target="EN-GB")

            pairs.append({
                "german": de.replace("\n", " "),
                "english": result.replace("\n", " "),
                "provider" : provider
            })

        return pairs

    return asyncio.run(_async_impl())

