import nltk
import asyncio
from nltk.tokenize import sent_tokenize
from googletrans import Translator
from audio_handler import make_bilingual_mp3, make_audio_byte

# Run once (or keep, it will not re-download)
nltk.download("punkt")
nltk.download("punkt_tab")

#
# def extract_sentences(file_path):
#     with open(file_path, "r", encoding="cp1252") as f:
#         text = f.read()
#
#     return sent_tokenize(text, language="german")


def make_sentence_pairs(original_text):
    async def _async_impl():
        german_sentences = sent_tokenize(original_text, language="german")
        translator = Translator()
        pairs = []

        for de in german_sentences:
            result = await translator.translate(de, src="de", dest="en")
            pairs.append({
                "german": de.replace("\n", " "),
                "english": result.text.replace("\n", " "),
                "audio_german":make_audio_byte(de, "de")
            })

        return pairs

    return asyncio.run(_async_impl())

# sentences = extract_sentences("text_de.txt")
pairs = make_sentence_pairs("")
make_bilingual_mp3(pairs,"all_pairs.mp3",2)

print("==========================================================================================")
for pair in pairs:
    print("GER: " + pair["german"])
    print("ENG: " + pair["english"])
    print("==========================================================================================")
