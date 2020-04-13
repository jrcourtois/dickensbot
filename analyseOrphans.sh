#! /bin/bash

cd /home/jr/dickensbot
export PYTHONPATH=/home/jr/dickensbot/lib
python3 bot/parseAllOrphans.py

# Preparing analysis
echo "Analyse Orphelins" > log.txt

python3 bot/analysis.py "Catégorie:Article orphelin depuis mars 2018" -d orph_2018-03.arch
python3 bot/analysis.py "Catégorie:Wikipédia:Tentative d'adoption en février 2018" -d tent_2018-02.arch
cat files/*.arch > files/arch/last.arch
mv files/*.arch files/arch/

python3 bot/analysis.py "Catégorie:Article orphelin depuis avril 2020" -d orph_2020-04.arch
mv files/*.arch files/arch/
