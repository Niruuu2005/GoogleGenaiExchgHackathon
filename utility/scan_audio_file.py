from google.cloud import speech

def transcribe_audio(file_path):
    client = speech.SpeechClient()

    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return transcripts

if __name__ == "__main__":
    file_path = "path/to/audio.wav"  # Replace with the input file path
    transcripts = transcribe_audio(file_path)
    for i, text in enumerate(transcripts, 1):
        print(f"Transcript {i}: {text}")
