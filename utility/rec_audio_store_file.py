import os
import sounddevice as sd
import numpy as np
import wave
import datetime

def record_audio(duration_seconds=5, sample_rate=16000, folder_path="resources/audio_recordings"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print(f"Recording audio for {duration_seconds} seconds...")

    audio_data = sd.rec(int(duration_seconds * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder_path, f"recording_{timestamp}.wav")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 2 bytes per sample (int16)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio recorded and saved to {filename}")
    return filename

if __name__ == "__main__":
    record_audio()
