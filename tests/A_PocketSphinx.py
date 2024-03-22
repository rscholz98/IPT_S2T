import os
from pocketsphinx import LiveSpeech, get_model_path

RATE = 16000  # Sampling rate

# Speech recognition with PocketSphinx
model_path = get_model_path()
speech = LiveSpeech(
    verbose=False,
    sampling_rate=RATE,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'cmudict-en-us.dict'),
    audio_file='./output.wav'  # Use the recorded audio file
)

for phrase in speech:
    print(phrase)
