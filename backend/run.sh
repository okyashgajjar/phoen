#!/bin/bash
source /home/yg/anaconda3/bin/activate base
pip install -r requirements.txt
uvicorn main:app --reload
