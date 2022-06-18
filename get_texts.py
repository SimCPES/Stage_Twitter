"""Programme permettant de récupérer les textes des tweets pour diminuer la quantité de données à manipuler"""

import json
import naya
import gzip
from unidecode import unidecode

tweets = []
data_register = []
# On choisit des dates réparties sur l'ensemble de la période électorale
dates = ["10-03-2022", "13-03-2022", "15-03-2022", "18-03-2022", "20-03-2022",
         "22-03-2022", "25-03-2022", "27-03-2022", "29-03-2022", "09-04-2022"]

for date in dates:
    # Pour chaque date sélectionnée on récupère les textes de 5 000 tweets répartis uniformément
    i = 0

    with gzip.open(f"./tweets/tweets_{date}.json.gz", mode="rt") as f:
        # On streame sur le fichier json en utilisant naya pour ne pas tout stocker en mémoire
        data = naya.stream_array(naya.tokenize(f))

        for status in data:
            if i == 50000:
                # On récupère 5 000 tweets par journée
                break
            if i%10 == 0:
                # On récupère le texte d'un tweet sur 10
                if "retweeted_status" in status:
                    try:
                        tweets.append(status["retweeted_status"]["extended_tweet"]["full_text"])
                    except KeyError:
                        tweets.append(status["retweeted_status"]["text"])
                else:
                    try:
                        tweets.append(status["extended_tweet"]["full_text"])
                    except:
                        tweets.append(status["text"])
            i += 1
            data_register.append(status)

i = 0        

# On récupère l'autre moitié des tweets parmi ceux n'ayant pas du tout de lien avec l'élection
with open("other_tweets.json") as f:
    data = naya.stream_array(naya.tokenize(f))
    
    for status in data:
        if i == 250000:
            break
        if i%5 == 0:
            if "retweeted_status" in status:
                try:
                    tweets.append(status["retweeted_status"]["extended_tweet"]["full_text"])
                except KeyError:
                    tweets.append(status["retweeted_status"]["text"])
            else:
                try:
                    tweets.append(status["extended_tweet"]["full_text"])
                except:
                    tweets.append(status["text"])
        i += 1
        data_register.append(status)

# On enregistre les tweets récupérés dans un fichier
with open("text_tweets_100000.json", "x") as f:
    f.write(json.dumps(data_register))
