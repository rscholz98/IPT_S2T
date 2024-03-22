import whisper
import pickle
import ffmpeg
import os

ffmpeg_path = "C:/ffmpeg/bin"  
os.environ['PATH'] += f':{os.path.dirname(ffmpeg_path)}'

model = whisper.load_model("base")

result = model.transcribe("output.wav", fp16=False)

print(result["text"])