"""Programme réalisant l'enregistrement de tweets en lien avec l'élection présidentielle grâce à du streaming avec filtrage"""

import tweepy
import json
from datetime import datetime
import os

# Ce sont les clés et token permettant une connexion sécurisée avec Twitter, elles ne doivent pas être partagées
consumer_key = "h****h"
consumer_secret = "n****7"
access_token = "1****D"
access_token_secret = "b****T"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# On initialise l'API avec les clés de sécurité
api = tweepy.API(auth)

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        if os.path.exists(f"./tweets/tweets_{datetime.today().strftime('%d-%m-%Y')}.json"):
            with open(f"./tweets/tweets_{datetime.today().strftime('%d-%m-%Y')}.json", mode="a") as f:
                tweet = json.dumps(status._json) # On récupère le tweet sous forme d'un dictionnaire
                # On met ce dictionnaire au bon format avec json puis on l'écrit dans le fichier
                f.write(tweet)
                f.write(", ") # Les tweets sont séparés par des virgules
        else:
            # Si aucun tweet n'a encore été enregistré pour cette journée on crée le fichier
            with open(f"./tweets/tweets_{datetime.today().strftime('%d-%m-%Y')}.json", mode="x") as f:
                f.write("[") # On commence le fichier par un crochet ouvrant
                tweet = json.dumps(status._json)
                f.write(tweet)
                f.write(", ")

def set_candidates():
    """Fonction permettant de récupérer les identifiants des comptes utilisés pour le filtrage"""
    candidats = []
    for line in open("comptes.txt"): # On charge les comptes sélectionnés
        candidats.append(line[:-1])

    dic = {}
    for candidat in candidats: # On récupère l'identifiant unique associé à chaque compte
        try:
            user = api.get_user(screen_name=candidat)
            dic[candidat] = user.id
        except:
            pass
    return dic

def set_keywords():
    """Fonction permettant de récupérer les mots-clés utilisés pour le filtrage"""
    keywords = []
    for line in open("mots-clés.txt"):
        keywords.append(line[:-1])
    return keywords

# On active le streamer avec les clés de sécurité
printer = IDPrinter(
  consumer_key, consumer_secret,
  access_token, access_token_secret
)


dic = set_candidates()
keywords = set_keywords()

try:
    printer.filter(follow=dic.values(), track=keywords, languages=["fr"])
except KeyboardInterrupt:
    print("Fin")
    quit()

