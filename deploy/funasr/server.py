"""Local SenseVoice service with an OpenAI-compatible transcription route."""
import os, tempfile
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile
from funasr import AutoModel
app=FastAPI(docs_url=None,redoc_url=None); _model=None
def get_model():
    global _model
    if _model is None: _model=AutoModel(model=os.getenv("FUNASR_MODEL","iic/SenseVoiceSmall"),trust_remote_code=True,disable_update=True)
    return _model
@app.get("/health")
def health(): return {"status":"ok","loaded":_model is not None}
@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile=File(...), model: str=Form("iic/SenseVoiceSmall")):
    suffix=Path(file.filename or "audio.wav").suffix
    with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as output: output.write(await file.read()); path=output.name
    try:
        rows=get_model().generate(input=path,cache={},language="auto",use_itn=True)
        return {"text":str(rows[0].get("text","")).strip() if rows else "","model":model}
    finally: Path(path).unlink(missing_ok=True)
