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

🌍 Supported Languages
English

Hindi

Bengali

Tamil

Telugu

Kannada

Gujarati

Punjabi

Chinese (Simplified)

Spanish

Japanese

Korean

Russian

German

French
---

🚀 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/real-time-voice-translator.git
cd real-time-voice-translator
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
python main.py
---

📁 Project Structure

css
Copy
Edit

real-time-voice-translator/
│
├── main.py              # Main application code
├── requirements.txt     # Dependencies
└── README.md            # Project description

🧪 How It Works
Select your Input Language (or use "auto").

Select your Output Language.

Click Start Translation to begin.

Speak into your microphone.

View live recognized speech and translated text.

Listen to the translated speech.

Use Pause / Resume as needed.

📌 Notes
This application requires an active internet connection for speech recognition, translation, and speech synthesis (since it uses Google APIs).

gTTS and SpeechRecognition services rely on external APIs — ensure stable network access for best performance.

Currently, gTTS does not support offline usage.
---
##🎓 Author
Sk Altab Hossen
B.Tech (Final Year), Information Technology
Email: skaltab.hossen03@gmail.com

## 📦 Requirements

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt


