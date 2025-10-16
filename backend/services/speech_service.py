import os
from datetime import datetime
from typing import Optional
from langchain.prompts import PromptTemplate
from TTS.api import TTS
from pydub import AudioSegment
from models import gemini_llm
from lib.utils import pretty_print
import whisper  # pip install openai-whisper

# === Initialize TTS model (Coqui TTS) ===
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

# === Initialize Whisper model for STT ===
whisper_model = whisper.load_model("base")  # tiny, base, small, medium, large


# === Generate story using LLM ===
def generate_story(topic: str) -> str:
    """
    Generate a short story for a given topic using Gemini LLM.
    """
    print(f"🎨 Generating story for topic: {topic}")

    story_prompt = PromptTemplate(
        input_variables=["topic"],
        template=(
            "You are a creative storyteller. Generate an engaging very short story (50-60 words) "
            "based on the following topic.\n"
            "Make the story captivating, well-structured with a beginning, middle, and end.\n"
            "Use vivid descriptions suitable for audio narration.\n"
            "Keep the language clear and easy to listen to.\n\n"
            "Topic: {topic}\n\nStory:"
        ),
    )

    prompt_text = story_prompt.format(topic=topic)
    response = gemini_llm.invoke(prompt_text)
    story = response.content.strip()
    print(f"✅ Story generated ({len(story)} characters)")
    return story


# === Convert text to audio (TTS) ===
def convert_text_to_audio(text: str, topic: str, audio_folder: str) -> dict:
    """
    Convert story text to MP3 audio using Coqui TTS.
    :param text: Story text
    :param topic: Topic for filename
    :param audio_folder: Folder to save MP3/WAV
    :return: dict with audio filename and path
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic[:30])
    audio_filename = f"story_{safe_topic}_{timestamp}.mp3"
    wav_path = os.path.join(audio_folder, audio_filename.replace(".mp3", ".wav"))
    audio_path = os.path.join(audio_folder, audio_filename)

    os.makedirs(audio_folder, exist_ok=True)

    print("🎙️ Converting story to audio...")

    # Generate WAV
    tts.tts_to_file(text=text, file_path=wav_path)

    # Convert WAV → MP3
    audio = AudioSegment.from_wav(wav_path)
    audio.export(audio_path, format="mp3", bitrate="192k")
    os.remove(wav_path)

    print(f"✅ Audio saved: {audio_path}")
    return {"audio_file": audio_filename, "audio_path": audio_path}


# === Main function called from Flask ===
def generate_story_with_audio(
    topic: str, session_id: Optional[str] = None, audio_folder: str = "static/audio"
) -> dict:
    """
    Generate story text and convert it to audio.
    Called from Flask route.
    """
    story = generate_story(topic)
    audio_info = convert_text_to_audio(story, topic, audio_folder)
    return {
        "story": story,
        "audio_file": audio_info["audio_file"],
        "audio_path": audio_info["audio_path"],
    }


# === Transcribe audio (STT) ===
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file to text using Whisper.
    :param file_path: Path to uploaded audio file
    :return: transcript string
    """
    print(f"🎤 Transcribing audio: {file_path}")
    result = whisper_model.transcribe(file_path)
    transcript = result.get("text", "").strip()
    print(f"✅ Transcription complete: {len(transcript)} characters")
    return transcript
