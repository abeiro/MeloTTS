from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import os, torch, io
from melo.api import TTS
import time
from huggingface_hub import hf_hub_download

# Initialize FastAPI
restapi = FastAPI()

# Function to download the checkpoint and config from Hugging Face
def download_hf_model():
    # Download the checkpoint.pth file
    ckpt_path = hf_hub_download(repo_id="tylermaister/SkyrimLikeVoices", filename="checkpoint.pth")

    # Download the config.json file
    custom_config_path = hf_hub_download(repo_id="tylermaister/SkyrimLikeVoices", filename="config.json")

    return ckpt_path, custom_config_path

# Load models at startup
device = 'cpu'
ckpt_path, custom_config_path = download_hf_model()

# Initialize the custom TTS model
model_custom = TTS(language='EN', config_path=custom_config_path, ckpt_path=ckpt_path, device=device)

# Add the custom model to the models dictionary
models = {
    'EN': TTS(language='EN', device=device),
    'SkyrimLikeVoices': model_custom
}

# Speaker IDs for each language
speaker_ids = models['SkyrimLikeVoices'].hps.data.spk2id

# Function to synthesize the speech
def synthesize(speaker, text, speed, language):
    try:
        start_time = time.time()
        bio = io.BytesIO()

        # Run TTS
        models['SkyrimLikeVoices'].tts_to_file(
            text,
            models['SkyrimLikeVoices'].hps.data.spk2id[speaker],
            bio,
            speed=speed,
            format='wav'
        )

        end_time = time.time()
        print(f"Synthesis completed in {end_time - start_time:.2f} seconds.")

        # Return the audio file
        bio.seek(0)
        return bio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in TTS synthesis: {str(e)}")

# Endpoint to get the list of speaker IDs
@restapi.get("/get_speaker_id_list")
async def get_speaker_id_list():
    try:
        return JSONResponse(content={"speaker_ids": list(speaker_ids.keys())})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving speaker IDs: {str(e)}")

# Endpoint to generate TTS audio
@restapi.post("/tts")
async def tts(speaker: str, text: str, speed: float = 1.0, language: str = 'EN'):
    
    if speaker not in models['SkyrimLikeVoices'].hps.data.spk2id:
        raise HTTPException(status_code=400, detail="Invalid speaker specified")
    
    audio = synthesize(speaker, text, speed, 'EN')

    # Return the audio as a stream response
    return StreamingResponse(audio, media_type="audio/wav")


@restapi.get("/tts")
async def tts(speaker: str, text: str, speed: float = 1.0, language: str = 'EN'):
    
    if speaker not in models['SkyrimLikeVoices'].hps.data.spk2id:
        raise HTTPException(status_code=400, detail="Invalid speaker specified")
    
    audio = synthesize(speaker, text, speed, 'EN')

    # Return the audio as a stream response
    return StreamingResponse(audio, media_type="audio/wav")
