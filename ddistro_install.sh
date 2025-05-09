#!/bin/bash

cd /home/dwemer/MeloTTS
python3 -m venv /home/dwemer/python-melotts
source /home/dwemer/python-melotts/bin/activate

echo "This will take a while so please wait."
pip install -r requirements.txt
echo "This download will take a while....be patient"
python -m unidic download
pip install -e .
python3 install_nltk.py
./conf.sh




