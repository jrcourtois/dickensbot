#! /bin/bash

export PYTHONPATH=/home/jr/dev/wiki/dickensbot/lib:/home/jr/dev/wiki/wikitools

echo "Mise à jour de la page de Discussion de JrCourtois - retrait des avertissements de pdd"
python3 bot/discussion.py
echo "Mise à jour des pages projets recensant les pages orphelines"
python3 bot/buildProjectPagesShort.py
echo "Parcours de tous les orphelins"
python3 bot/parseAllOrphans.py
echo "Récupération des orphelins de la page des orphelins"
python3 bot/orphan.py
echo "Adoption des orphelins tels que remontés via parseAllOrphans"
python3 bot/adopt.py
echo "Recherche des orphelins récemment créés"
python3 bot/trackNew.py
echo "Mise à jour des pages mensuelles d'adoption/tentative"
python3 bot/analysisCompare.py
