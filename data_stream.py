"""Programme réalisant l'enregistrement de tweets en lien avec l'élection présidentielle grâce à du streaming avec filtrage"""

import tweepy  # Module tweepy pour utiliser l'API Twitter
import json
from datetime import datetime
import os

# Ce sont les clés et token permettant une connexion sécurisée avec Twitter, elles ne doivent pas être partagées
consumer_key = "h****h"
consumer_secret = "n****7"
access_token = "1****D"
access_token_secret = "b****T"

# Fonctions permettant de se connecter de manière sécurisée en utilisant les clés de sécurité personnelles
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# On initialise l'API avec les clés de sécurité ce qui crée une connexion sécurisée avec Twitter
api = tweepy.API(auth)

class IDPrinter(tweepy.Stream):
    """Classe permettant de gérer les tweets retournés par le streamer"""

    def on_status(self, status):
        """Méthode permettant de manipuler les tweets retournés par le streamer"""
        # On ajoute le tweet au fichier du jour. Si c'est le premier tweet enregistré de la journée on crée le fichier du jour
        # et on l'ajoute
        if os.path.exists(f"./tweets/tweets_{datetime.today().strftime('%d-%m-%Y')}.json"): # Si le fichier du jour existe
            with open(f"./tweets/tweets_{datetime.today().strftime('%d-%m-%Y')}.json", mode="a") as f:
                tweet = json.dumps(status._json) # On récupère le tweet sous forme d'un dictionnaire
                # On met ce dictionnaire au bon format avec json puis on l'écrit dans le fichier
                f.write(tweet)
                f.write(", ") # Dans un fichier, les tweets sont séparés par des virgules
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

# On récupère les comptes et mots-clés utilisés pour le filtrage en utilisant les fonctions ci-dessus
dic = set_candidates()
keywords = set_keywords()

# Le streamer tourne en continu jusqu'à être arrêté 
try:
    # 'follow' correspond au filtre par compte
    # 'track' correspond au filtre par mots-clés
    printer.filter(follow=dic.values(), track=keywords, languages=["fr"])
except KeyboardInterrupt: # Pour interrompre le programme proprement
    print("Fin")
    quit()

