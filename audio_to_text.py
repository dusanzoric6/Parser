import whisper

# load a model: "base", "small", "medium", or "large"
model = whisper.load_model("medium")

# path to your German audio file
audio_path = "audio_files/crossYufix_12_03.m4a"
title = audio_path.split("/")[1].split(".m4a")[0]

# transcribe
result = model.transcribe(audio_path, language="de")

# extract text
text = result["text"]

# save to a text file
output_file = f"textFiles/{title}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Transcription saved to", output_file)
