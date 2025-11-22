# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .scoring import score_transcript
import tempfile
import os

# Import whisper lazily to avoid heavy import if not used right away
import whisper

app = FastAPI(title="Nirmaan Rubric Scorer API (with ASR)")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Whisper model once at startup (choose model size; base is a good balance)
WHISPER_MODEL_NAME = os.environ.get("WHISPER_MODEL", "base")
print("Loading Whisper model:", WHISPER_MODEL_NAME)
whisper_model = whisper.load_model(WHISPER_MODEL_NAME)
print("Whisper model loaded.")

class TranscriptInput(BaseModel):
    transcript: str
    duration_sec: float = 60.0

@app.get("/")
def root():
    return {"message": "Nirmaan Rubric Scorer Running"}

@app.post("/score")
def score_text(data: TranscriptInput):
    if not data.transcript or data.transcript.strip() == "":
        raise HTTPException(status_code=400, detail="Provide non-empty transcript")
    result = score_transcript(data.transcript, data.duration_sec)
    return result

@app.post("/score_audio")
async def score_audio(file: UploadFile = File(...), duration_sec: float = Form(...)):
    """
    Accept an audio file upload (wav/mp3/m4a etc.) and duration (seconds).
    The endpoint will:
      1) save the audio to a temp file
      2) run Whisper transcription
      3) call score_transcript(transcript, duration_sec)
      4) return transcript + scoring JSON
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save to a temp file
    suffix = os.path.splitext(file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # Transcribe using whisper
        # Note: you can pass options like language="en" or task="transcribe"
        result = whisper_model.transcribe(tmp_path, language="en")
        transcript = result.get("text", "").strip()

        # If duration not provided or 0, estimate from whisper result segments
        # Otherwise use provided duration_sec
        if duration_sec is None or duration_sec <= 0:
            # try to estimate using segments timestamps if available
            segments = result.get("segments", [])
            if segments:
                # last segment end time
                duration_sec_est = segments[-1].get("end", None)
                if duration_sec_est:
                    duration_sec = float(duration_sec_est)
            # fallback: keep as 60 seconds if none available
            if duration_sec is None or duration_sec <= 0:
                duration_sec = 60.0

        # Score the transcript using existing rubric scoring
        scoring = score_transcript(transcript, duration_sec)

        return {
            "filename": file.filename,
            "transcript": transcript,
            "transcription_meta": {
                "model": WHISPER_MODEL_NAME,
                "whisper_result_keys": list(result.keys()),
            },
            "duration_sec_used": duration_sec,
            "score": scoring
        }
    finally:
        # cleanup temp file
        try:
            os.remove(tmp_path)
        except Exception:
            pass
