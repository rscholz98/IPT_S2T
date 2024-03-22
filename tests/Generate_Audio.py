import wave
import pyaudio

# Configuration for PyAudio to capture from microphone
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 16000  # Sampling rate
CHUNK = 1024  # Number of frames per buffer

audio = pyaudio.PyAudio()

# Start the microphone stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

try:
    # Capture data from the microphone for a few seconds
    for i in range(0, int(RATE / CHUNK * 20)):
        data = stream.read(CHUNK)
        frames.append(data)
finally:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

print("Finished recording.")

# Save the captured data to a WAV file
wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()