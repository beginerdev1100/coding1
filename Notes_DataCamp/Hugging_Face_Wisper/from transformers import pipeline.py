from transformers import pipeline
import soundcard as sc
import soundfile as sf

def record_audio(seconds, filename, rate=16000):
    mic = sc.default_microphone()
    audio = mic.record(samplerate=rate, numframes=int(seconds * rate), channels=1)
    sf.write(filename, audio, rate)
    print(f"Saved: {filename}")


def text_trans(file):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo")

    print(pipe(file, language='en')['text'], end='')

record_audio(10, "output.wav")