cd /home/dwemer/MeloTTS

source /home/dwemer/python-melotts/bin/activate

cd melo
uvicorn restapig:restapi --reload --host 0.0.0.0 --port 8084 &> log.txt &


