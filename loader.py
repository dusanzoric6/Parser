import deepl
import nltk
import asyncio
from nltk.tokenize import sent_tokenize
from googletrans import Translator
from audio_handler import make_bilingual_mp3, make_audio_byte

# Run once (or keep, it will not re-download)


# SifrazaDeepl6!
# 0de8b866-1e19-4e03-be74-88f457d89ccd:fx


# translator = Translator()
translator = deepl.Translator("0de8b866-1e19-4e03-be74-88f457d89ccd:fx")

def translate_de_to_en(text):
    result = translator.translate_text(
        text,
        source_lang="DE",
        target_lang="EN-US"
    )
    return result.text

def make_sentence_pairs(original_text):
    async def _async_impl():
        nltk.download("punkt")
        nltk.download("punkt_tab")
        german_sentences = sent_tokenize(original_text, language="german")
        pairs = []

        for de in german_sentences:
            # result = await translator.translate(de, src="de", dest="en")
            result = translator.translate_text(de,source_lang="DE",target_lang="EN-GB")

            pairs.append({
                "german": de.replace("\n", " "),
                "english": result.text.replace("\n", " "),
                "audio_german":make_audio_byte(de, "de")
            })

        return pairs

    return asyncio.run(_async_impl())

