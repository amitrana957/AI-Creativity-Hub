# AI-Creativity-Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![React Native](https://img.shields.io/badge/React_Native-Expo-blue)](https://reactnative.dev/)

**AI-Creativity-Hub** is a multi-modal AI platform that allows users to interact with AI in various ways:

- **Text Chat** – Ask questions and get AI-generated answers
- **Image Generation** – Generate images from text prompts
- **Audio Transcription** – Convert audio to text
- **Multimodal Tasks** – Combine text, image, and audio inputs for AI processing

The project is a **full-stack solution** with a **React Native frontend** and a **Python Flask backend**.

---

## Features

- Cross-platform mobile app (iOS & Android)
- Modular AI services: text, image, audio, multimodal
- Clean and reusable UI with a professional design
- Easily extendable backend for new AI features

---

## Tech Stack

**Frontend:**

- React Native (Expo)
- React Navigation
- TypeScript

**Backend:**

- Python 3.10+
- Flask
- Flask-RESTful (optional)
- Pydantic (optional, for data validation)

---

## Setup & Installation

### Frontend (React Native)

```bash
cd frontend
npm install
npm start
```

### Backend (Flask)

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scriptsctivate

pip install -r requirements.txt

# Set environment variables
# Linux/macOS
export FLASK_APP=main.py
export FLASK_ENV=development
# Windows (PowerShell)
# $env:FLASK_APP="main.py"
# $env:FLASK_ENV="development"

flask run
```

---

## Usage

1. Start the backend server (`flask run`)
2. Start the frontend app using Expo (`npm start`)
3. Use the app to:
   - Chat with AI
   - Generate images from prompts
   - Transcribe audio
   - Perform multimodal AI tasks

---

## API Endpoints (Flask)

- **POST /api/text-chat**

  - **Input:** JSON `{ "text": "your question here" }`
  - **Output:** JSON `{ "answer": "AI response" }`

- **POST /api/image-gen**

  - **Input:** JSON `{ "prompt": "image description" }`
  - **Output:** JSON `{ "image_url": "https://..." }`

- **POST /api/audio-transcribe**

  - **Input:** Multipart/form-data audio file
  - **Output:** JSON `{ "transcription": "transcribed text" }`

- **POST /api/multimodal**
  - **Input:** JSON `{ "text": "...", "image": "...", "audio": "..." }`
  - **Output:** JSON `{ "result": "AI output" }`

---

## Example API Requests (cURL)

```bash
# Text Chat
curl -X POST http://localhost:5000/api/text-chat -H "Content-Type: application/json" -d '{"text": "Hello AI!"}'

# Image Generation
curl -X POST http://localhost:5000/api/image-gen -H "Content-Type: application/json" -d '{"prompt": "A futuristic city skyline"}'

# Audio Transcription
curl -X POST http://localhost:5000/api/audio-transcribe -F "file=@/path/to/audio.mp3"

# Multimodal
curl -X POST http://localhost:5000/api/multimodal -H "Content-Type: application/json" -d '{"text": "Describe this image", "image": "image_url_here"}'
```

---

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs/features.

- Follow standard GitHub workflow: Fork → Branch → PR → Merge
- Ensure code is clean, readable, and commented
- Add tests for any new features

---

## License

MIT License
