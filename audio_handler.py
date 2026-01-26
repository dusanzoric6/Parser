from gtts import gTTS
from pydub import AudioSegment
import io


def tts_to_audiosegment(text, lang):
    """
    Convert text to speech and return AudioSegment (binary audio)
    """
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return AudioSegment.from_file(mp3_fp, format="mp3")


def make_bilingual_mp3(
    pairs,
    output_file="output.mp3",
    pause_seconds=3
):
    final_audio = AudioSegment.silent(duration=0)
    counter = 1
    for pair in pairs:
        german_audio = tts_to_audiosegment(pair["german"], "de")
        english_audio = tts_to_audiosegment(pair["english"], "en")

        pause = AudioSegment.silent(duration=pause_seconds * 1000)
        end_pause = AudioSegment.silent(duration=1000)  # 1 sec between pairs

        # Append to final audio
        final_audio += german_audio
        final_audio += pause
        final_audio += english_audio
        final_audio += pause
        final_audio += german_audio
        final_audio += pause

        final_audio += end_pause

        print((counter / len(pairs)) * 100)
        counter += 1

    # Export MP3
    final_audio.export(output_file, format="mp3")

    print(f"MP3 created: {output_file}")

def make_audio_byte(
    text,
    lang="de"
):
    """
    Uses tts_to_audiosegment and returns MP3 audio bytes
    """
    audio_segment = tts_to_audiosegment(text, lang)

    buffer = io.BytesIO()
    audio_segment.export(buffer, format="mp3")
    buffer.seek(0)

    return buffer.read()

