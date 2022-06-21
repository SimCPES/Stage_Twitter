"""Fichier réalisant la finalisation du fichier de tweets du jour en lui donnant le format voulu et en le compressant"""

#!/bin/bash

# Ce programme s'exécute tous les jours à minuit dix

DATE=$(date --date='1 day ago' +%d-%m-%Y);  # On récupère la date du jour précédent car il est plus de minuit au moment de l'exécution
HOUR=$(date +%T);


# On 'ferme' le fichier en lui donnant le format d'une liste Python, c'est à dire que l'on retire la virgule en trop
# et on ajoute un crochet fermant à la fin du fichier
truncate -s -2 ./tweets/tweets_$DATE.json  
echo ] >> ./tweets/tweets_$DATE.json

# On compresse le fichier pour qu'il prenne moins de place
gzip -v ./tweets/tweets_$DATE.json





