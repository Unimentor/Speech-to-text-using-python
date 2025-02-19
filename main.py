import speech_recognition as sr
import threading
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to capture live audio from the microphone
def listen_to_microphone():
    with sr.Microphone() as source:
        # Adjust for ambient noise and wait for a moment to ensure the microphone is ready
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Please speak something...")
        audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        print("Recording complete.")
        return audio_data

# Function to stop recording on user input
def stop_recording():
    input("Press Enter to stop recording...\n")
    global recording
    recording = False

# Start the stop recording thread
recording = True
stop_thread = threading.Thread(target=stop_recording)
stop_thread.start()

# Capture audio until the user stops the recording
audio_data_list = []
while recording:
    audio_data = listen_to_microphone()
    audio_data_list.append(audio_data)

# Combine all audio data into one
combined_audio_data = sr.AudioData(
    b''.join([audio.get_raw_data() for audio in audio_data_list]),
    audio_data_list[0].sample_rate,
    audio_data_list[0].sample_width
)

# Convert the captured audio to text
try:
    text = recognizer.recognize_google(combined_audio_data)
    print("Converted Text: ", text)
    
    # Write the converted text to a file
    with open("converted_text.txt", "w") as text_file:
        text_file.write(text)
    print("Text has been written to converted_text.txt")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")