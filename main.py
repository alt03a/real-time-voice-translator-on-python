import os
import uuid
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text
import queue
import io
import tempfile

# Create GUI
win = tk.Tk()
win.geometry("700x450")
win.title("Real-Time Voice🎙 Translator🔊")
win.configure(bg="#2C3E50")

# Text Display
input_label = tk.Label(win, text="Recognized Text ⮯", bg="#2C3E50", fg="white", font=("Arial", 11, "bold"))
input_label.pack()
input_text = tk.Text(win, height=5, width=50, bg="#34495E", fg="white", font=("Arial", 10))
input_text.pack()

output_label = tk.Label(win, text="Translated Text ⮯", bg="#2C3E50", fg="white", font=("Arial", 11, "bold"))
output_label.pack()
output_text = tk.Text(win, height=5, width=50, bg="#34495E", fg="white", font=("Arial", 10))
output_text.pack()

tk.Label(win, text="", bg="#2C3E50").pack()

# Language Dropdowns
language_codes = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Spanish": "es", "Chinese (Simplified)": "zh-CN",
    "Russian": "ru", "Japanese": "ja", "Korean": "ko", "German": "de", "French": "fr",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Gujarati": "gu", "Punjabi": "pa"
}
language_names = list(language_codes.keys())

input_lang_label = tk.Label(win, text="Select Input Language:", bg="#2C3E50", fg="white")
input_lang_label.pack()
input_lang = ttk.Combobox(win, values=language_names)
input_lang.bind("<<ComboboxSelected>>", lambda e: input_lang.set(language_codes[e.widget.get()]))
if input_lang.get() == "":
    input_lang.set("auto")
input_lang.pack()

tk.Label(win, text="▼", bg="#2C3E50", fg="white").pack()

output_lang_label = tk.Label(win, text="Select Output Language:", bg="#2C3E50", fg="white")
output_lang_label.pack()
output_lang = ttk.Combobox(win, values=language_names)
output_lang.bind("<<ComboboxSelected>>", lambda e: output_lang.set(language_codes[e.widget.get()]))
if output_lang.get() == "":
    output_lang.set("en")
output_lang.pack()

tk.Label(win, text="", bg="#2C3E50").pack()

# Flags & Recognizer
keep_running = False
is_paused = False
recognizer = sr.Recognizer()
audio_queue = queue.Queue()

# Pre-initialize translator to avoid repeated initialization
translator = None
current_lang_pair = None

# Optimize recognizer settings for faster processing
recognizer.energy_threshold = 4000  # Higher threshold for faster triggering
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.5  # Shorter pause threshold
recognizer.phrase_threshold = 0.3  # Shorter phrase threshold

# Function to play & delete .mp3 with optimized temp file handling
def play_and_delete(audio_data, lang):
    try:
        # Use temporary file in memory-backed location if available
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
        # Save audio data
        voice = gTTS(audio_data, lang=lang, slow=False)  # Set slow=False for faster speech
        voice.save(tmp_path)
        
        # Play immediately
        playsound(tmp_path)
    except Exception as e:
        print(f"Audio playback error: {e}")
    finally:
        # Clean up
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except:
            pass

def update_translation():
    global keep_running, is_paused, translator, current_lang_pair
    mic = sr.Microphone()

    def capture_audio():
        with mic as source:
            # Faster ambient noise adjustment
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            while keep_running:
                try:
                    # Reduced phrase time limit for faster processing
                    audio = recognizer.listen(source, phrase_time_limit=2, timeout=1)
                    audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    win.after(0, lambda: output_text.insert(tk.END, f"Mic Error: {str(e)}\n"))

    def process_audio():
        global translator, current_lang_pair
        
        while keep_running:
            if not audio_queue.empty():
                audio = audio_queue.get()
                try:
                    # Use Google's faster recognition with reduced timeout
                    speech_text = recognizer.recognize_google(audio, language=input_lang.get() if input_lang.get() != "auto" else None)
                    
                    # Optimize transliteration - only if needed
                    code = input_lang.get()
                    if code not in ('auto', 'en'):
                        try:
                            speech_text = transliterate_text(speech_text, lang_code=code)
                        except:
                            pass  # Continue without transliteration if it fails
                    
                    # Update UI immediately
                    win.after(0, lambda text=speech_text: input_text.insert(tk.END, f"{text}\n"))

                    if speech_text.lower() in {'exit', 'stop'}:
                        break

                    # Optimize translator reuse
                    lang_pair = (input_lang.get(), output_lang.get())
                    if translator is None or current_lang_pair != lang_pair:
                        translator = GoogleTranslator(source=input_lang.get(), target=output_lang.get())
                        current_lang_pair = lang_pair
                    
                    # Translate with existing translator instance
                    translated = translator.translate(speech_text)
                    
                    # Update UI immediately
                    win.after(0, lambda text=translated: output_text.insert(tk.END, f"{text}\n"))

                    # Start audio generation in parallel (non-blocking)
                    threading.Thread(target=play_and_delete, args=(translated, output_lang.get()), daemon=True).start()

                except sr.UnknownValueError:
                    win.after(0, lambda: output_text.insert(tk.END, "Could not understand!\n"))
                except Exception as e:
                    win.after(0, lambda err=str(e): output_text.insert(tk.END, f"Error: {err}\n"))

    # Start both threads with higher priority
    capture_thread = threading.Thread(target=capture_audio, daemon=True)
    process_thread = threading.Thread(target=process_audio, daemon=True)
    
    capture_thread.start()
    process_thread.start()

# Button functions
def run_translator():
    global keep_running, is_paused
    if not keep_running:
        keep_running = True
        is_paused = False
        update_translation()

def pause_translation():
    global keep_running, is_paused
    keep_running = False
    is_paused = True

def resume_translation():
    global keep_running, is_paused
    if is_paused:
        keep_running = True
        is_paused = False
        update_translation()

# Buttons
tk.Button(win, text="Start Translation", command=run_translator, bg="#27ae60", fg="white", font=("Arial", 10, "bold")).place(relx=0.25, rely=0.9, anchor="c")
tk.Button(win, text="⏸ Pause", command=pause_translation, bg="#f39c12", fg="white", font=("Arial", 10, "bold")).place(relx=0.5, rely=0.9, anchor="c")
tk.Button(win, text="▶ Resume", command=resume_translation, bg="#2980b9", fg="white", font=("Arial", 10, "bold")).place(relx=0.75, rely=0.9, anchor="c")

# Run GUI
win.mainloop()
