#! /bin/bash

export PYTHONPATH=/home/jr/dev/wiki/dickensbot/lib:/home/jr/dev/wiki/wikitools

python3 bot/orphan.py
python3 bot/adopt.py
python3 bot/discussion.py
python3 bot/trackNew.py
python3 bot/analysisCompare.py
