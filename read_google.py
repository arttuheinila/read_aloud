import subprocess
from langdetect import detect, DetectorFactory
from gtts import gTTS
import os
import vlc
import time

DetectorFactory.seed = 0  # Make language detection deterministic

def get_clipboard_content():
    result = subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True)
    return result.stdout.strip()

def add_punctuation_to_text(text):
    # Replace newlines with a period followed by a newline
    return text.replace('\n', '.\n')

def read_clipboard_content():
    content = get_clipboard_content()

    if not content:
        print("Clipboard seems to be empty")
        return

    # Check if the content is a URL
    if content.startswith("http"):
        print("It seems to be a webpage")
        return

    # Detect the language using the first 10 words
    words = content.split()[:10]
    if not words:
        print("Clipboard seems to be empty")
        return

    sample_text = ' '.join(words)
    language = detect(sample_text)

    if language == "en":
        lang_code = "en"
    elif language == "fi":
        lang_code = "fi"
    else:
        print("Language not supported for reading")
        return
    
    # Add punctuation to the content
    content_with_punctuation = add_punctuation_to_text(content)
    
    # Convert text to speech
    try:
        tts = gTTS(text=content_with_punctuation, lang=lang_code, slow=False)
        tts.save("temp.mp3")

        # Initialize VLC player
        player = vlc.MediaPlayer("temp.mp3")
        
        # Set playback speed to 1.25x
        player.set_rate(1.25)

        # Start playing
        print("Starting playback...")
        player.play()

        # Wait for the player to actually start playing
        time.sleep(1)  # Wait a moment to allow playback to start

        # Check if the player started successfully
        state = player.get_state()
        print(f"Player state after starting: {state}")
        
        if state != vlc.State.Playing:
            print("Error: Player did not start correctly.")
            return

        # Keep script running while the player is playing
        while player.get_state() == vlc.State.Playing:
            try:
                time.sleep(0.1)  # Sleep a little to prevent high CPU usage
            except KeyboardInterrupt:
                print("\nReading aborted by user.")
                player.stop()
                break

    except KeyboardInterrupt:
        print("\nScript aborted by user.")
    finally:
        if os.path.exists("temp.mp3"):
            os.remove("temp.mp3")


if __name__ == "__main__":
    try:
        read_clipboard_content()
    except KeyboardInterrupt:
        print("\nScript aborted by user.")