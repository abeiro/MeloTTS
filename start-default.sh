python3 -m venv .venv
source .venv/bin/activate
cd melo
uvicorn restapi:restapi --reload --host 0.0.0.0 --port 8084

