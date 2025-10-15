import os
from datetime import datetime
from typing import Optional
from langchain.prompts import PromptTemplate
from TTS.api import TTS
from lib.utils import pretty_print
from models import gemini_llm


# --- Initialize TTS model (Coqui TTS - open source) ---
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

pretty_print(tts.languages)

# --- Create directory for audio files ---
AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


def generate_story(topic: str) -> str:
    """
    Generate a story using Mistral LLM

    Args:
        topic: The topic/theme for the story

    Returns:
        Generated story text
    """
    print(f"🎨 Generating story for topic: {topic}")

    # Simple prompt template without chat history
    story_prompt = PromptTemplate(
        input_variables=["topic"],
        template="""You are a creative storyteller. Generate an engaging short story (200-300 words) based on the following topic.
                Make the story captivating, well-structured with beginning, middle, and end.
                Use vivid descriptions suitable for audio narration.
                Keep the language clear and easy to listen to.

                Topic: {topic}

                Story:""",
    )

    # Generate story
    prompt_text = story_prompt.format(topic=topic)
    response = gemini_llm.invoke(prompt_text)

    story = response.content.strip()

    print(f"✅ Story generated ({len(story)} characters)")
    return story


def convert_text_to_audio(text: str, topic: str) -> dict:
    """
    Convert text to audio using TTS and save as MP3

    Args:
        text: Story text to convert
        topic: Topic used for filename

    Returns:
        dict with audio filename and path
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create safe filename from topic (remove special chars)
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic[:30])
    audio_filename = f"story_{safe_topic}_{timestamp}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    print(f"🎙️  Converting story to audio...")

    # Generate audio and save as WAV first
    wav_path = audio_path.replace(".mp3", ".wav")
    tts.tts_to_file(text=text, file_path=wav_path)

    # Convert WAV to MP3 using pydub
    try:
        from pydub import AudioSegment

        audio = AudioSegment.from_wav(wav_path)
        audio.export(audio_path, format="mp3", bitrate="192k")
        os.remove(wav_path)  # Remove temporary WAV file
        print(f"✅ Audio saved as MP3: {audio_path}")
    except ImportError:
        # If pydub is not available, keep as WAV and rename
        print("⚠️  pydub not found, saving as WAV instead")
        os.rename(wav_path, audio_path.replace(".mp3", ".wav"))
        audio_filename = audio_filename.replace(".mp3", ".wav")
        audio_path = audio_path.replace(".mp3", ".wav")

    return {"audio_file": audio_filename, "audio_path": audio_path}


def generate_story_with_audio(topic: str, session_id: Optional[str] = None) -> dict:
    """
    Main function: Generate story and convert to audio

    Args:
        topic: The topic/theme for the story

    Returns:
        dict with story text, audio filename, and path
    """
    # Step 1: Generate story
    story = generate_story(topic)

    # Step 2: Convert to audio
    audio_info = convert_text_to_audio(story, topic)

    return {
        "story": story,
        "audio_file": audio_info["audio_file"],
        "audio_path": audio_info["audio_path"],
    }


generate_story_with_audio("Cat and Dog")
