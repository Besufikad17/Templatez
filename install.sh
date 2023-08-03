#!/bin/bash
git clone https://github.com/Besufikad17/Templatez.git &
cd Templatez &
python3 -m venv venv &
source venv/bin/activate &
pip install -r requirements.txt &
python templatez.py &
deactivate
