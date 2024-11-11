#!/bin/sh

python3 -m venv venv

source venv/bin/activate
pip install -r requirements.txt

cd api/src
uvicorn main:app --host 0.0.0.0 --port 5500 --reload &

cd ../../

cd client
streamlit run stream_lit.py
