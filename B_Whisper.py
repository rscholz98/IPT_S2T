import whisper
import pickle

model = whisper.load_model("base")

result = model.transcribe("output.wav")

print(result["text"])