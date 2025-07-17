# real-time-voice-translator-on-python
🎙 Real-Time Speech Translator App using Python
 # 🎙️ Real-Time Voice Translator 🔊

A real-time voice translation application built using Python that captures speech via microphone, translates it into a selected language, and plays back the translated speech instantly. It uses Google APIs for translation and speech synthesis.

---

## 🧠 Features

- 🎤 Real-time voice recognition using `SpeechRecognition`
- 🌐 Auto or manual language selection for input and output
- 🔄 Instant translation using `deep_translator`
- 🔊 Spoken translation output via `gTTS`
- 📋 Live GUI display of recognized and translated text
- ⏸ Pause / ▶ Resume control
- 🖥️ User-friendly GUI using Tkinter
- 🧹 Automatic cleanup of audio files after playback

---

## 💻 Technologies Used

- Python 3
- Tkinter (GUI)
- gTTS (Google Text-to-Speech)
- deep_translator (Google Translate API)
- SpeechRecognition
- playsound
- Googletransliteration
- threading, queue, tempfile, and other Python standard modules

---

## 📦 Requirements

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt

