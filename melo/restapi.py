from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
import os, torch, io
from melo.api import TTS
import time

# Initialize FastAPI restapi
restapi = FastAPI()

# Load models at startup
device = 'cpu'
models = {
    'EN': TTS(language='EN', device=device)
}

ckpt_path = "data/SkyrimLikeVoices/checkpoint.pth"
custom_config_path = os.path.join(os.path.dirname(ckpt_path), 'config.json')
model_custom = TTS(language='EN', config_path=custom_config_path, ckpt_path=ckpt_path, device=device)

# Add the custom model to the dictionary
models['SkyrimLikeVoices'] = model_custom

# Speaker IDs for each language
speaker_ids = models['SkyrimLikeVoices'].hps.data.spk2id
# print(speaker_ids.keys())
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

