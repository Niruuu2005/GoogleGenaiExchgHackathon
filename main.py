import os
import time
from utility.webscrapper import scrape_website_content as scrape_website
from LLM.gemini import generate_llm_content
from google.cloud import speech
import sounddevice as sd
import wave
import datetime
import numpy as np

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

def call_llm_for_analysis(text):
    """Centralized LLM call for any text content."""
    llm_prompt = (
        f"Analyze the following text:\n\n"
        f"Create a concise, easy-to-understand summary of the main points and key takeaways.\n\n"
        f"Text to analyze:\n\n{text}"
    )
    print("\nSending content to the LLM for analysis...\n")
    llm_response = generate_llm_content(
        topic=llm_prompt,
        format_req="a detailed analysis in markdown",
        constraints="Be direct and specific. Use bullet points for clarity.",
        persona="You are a meticulous content analyst and fact-checker."
    )
    return llm_response

def analyze_website():
    print("Welcome to the Web Content Analyzer!")
    url = input("Please enter the URL of the website you want to analyze: ")
    scraped_content = scrape_website(url)
    if not scraped_content:
        print("Failed to scrape content. Exiting.")
        return
    print("\n--- Scraped Content (Summary) ---")
    print(scraped_content[:500] + "..." if len(scraped_content) > 500 else scraped_content)
    print("-" * 50)
    llm_response = call_llm_for_analysis(scraped_content)
    print("\n--- LLM Summarization ---")
    print(llm_response)
    print("-" * 50)

def analyze_audio():
    print("Welcome to the Audio Transcription Service!")
    print("Choose an option:")
    print("1. Record audio now")
    print("2. Provide path to existing audio file")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        try:
            duration = int(input("Enter recording duration in seconds (default 5): ") or "5")
        except ValueError:
            duration = 5
        file_path = record_audio(duration_seconds=duration)
    elif choice == "2":
        file_path = input("Please enter the path to the audio file you want to transcribe: ").strip()
        if not os.path.exists(file_path):
            print("File does not exist. Exiting audio analysis.")
            return
    else:
        print("Invalid choice. Returning to main menu.")
        return

    print("\nTranscribing audio...\n")
    try:
        transcripts = transcribe_audio(file_path)
        combined_text = " ".join(transcripts)
        print("--- Raw Transcription ---")
        for i, text in enumerate(transcripts, 1):
            print(f"Transcript {i}: {text}")
        print("-" * 50)
        if combined_text.strip():
            llm_response = call_llm_for_analysis(combined_text)
            print("\n--- LLM Summarization of Transcript ---")
            print(llm_response)
            print("-" * 50)
        else:
            print("No transcript text available for LLM processing.")
    except Exception as e:
        print(f"An error occurred during transcription: {e}")

def main():
    while True:
        print("\nSelect an option:")
        print("1. Analyze website content")
        print("2. Transcribe audio file (record or path) and analyze")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            analyze_website()
        elif choice == "2":
            analyze_audio()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
