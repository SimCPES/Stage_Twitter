import json
import csv
from unidecode import unidecode

# Liste des comptes sélectionnés
comptes = \
["JLMelenchon", "MLP_officiel", "RNational_off", "avecvous", "FranceInsoumise", "Anne_Hidalgo",
"vprecresse", "yjadot", "ZemmourEric", "AEC_LeProgramme", "enmarchefr", "2022avecHidalgo",
"lesRepublicains"]

# Mots-clés permettant de déterminer si un tweet est en lien avec l'élection
mots = ["presidentiel", "presidentielle", "vote", "programme","#presidentielles2022",
        "#presidentielle2022", "sondage", "le pen", "meeting", "#remigration", "electeur",
        "second tour", "elire", "election", "extreme droite", "pourcent", "melenchon",
        "premier tour", "campagne", "jadot", "septennat", "#electionpresidentielle2022",
        "melenchoniste", "matignon", "legislative", "lrem", "lfi"]

# On charge les textes des tweets à étiqueter
with open("tweets_200000_t4_2.json") as f:
    data = json.load(f)        

def intweet(tweet):
    """Fonction déterminant si un tweet est en lien avec l'élection ou pas, selon les critères choisis"""
    # On récupère le texte du tweet, selon qu'il s'agit d'un retweet et selon sa taille
    if "retweeted_status" in tweet:
        try:
            t = tweet["retweeted_status"]["extended_tweet"]["full_text"]
        except KeyError:
            t = tweet["retweeted_status"]["text"]
    else:
        try:
            t = tweet["extended_tweet"]["full_text"]
        except:
            t = tweet["text"]
    # On vérifie si l'un des comptes sélectionnés est mentionné dans le tweet
    try:
        for compte in tweet["extended_tweet"]["entities"]["user_mentions"]:
            if compte["screen_name"] in comptes:
                return True
    except KeyError:
        for compte in tweet["entities"]["user_mentions"]:
            if compte["screen_name"] in comptes:
                return True
    # On vérifie si l'un des mots-clés est présent dans le tweet
    for mot in mots:
        try:
            if mot in unidecode(t.lower()):
                 return True
        except Exception as e:
            print(e)
    return False

with open("tweets_200000_t4_2.csv", mode="x") as g:
    # Pour chaque tweet on cherche l'étiquette correspondante
    writer = csv.writer(g)
    for tweet in data:
        if "retweeted_status" in tweet and tweet["retweeted_status"]["user"]["screen_name"] in comptes:
        # Si le tweet est un retweet d'un compte sélectionné il est en lien avec l'élection
            writer.writerow([1])
        elif tweet["user"]["screen_name"] in comptes:
        # Si le tweet est issu d'un compte sélectionné il est en lien avec l'élection
            writer.writerow([1])
        elif tweet["in_reply_to_screen_name"] in comptes:
        # Si le tweet est une réponse à un compte sélectionné il est en lien avec l'élection
            writer.writerow([1])
        elif intweet(tweet):
        # On vérifie les conditions de la fonction précédemment définie
            writer.writerow([1])
        else:
        # Si aucune de ces conditions n'est remplie le tweet n'a pas de lien avec l'élection
            writer.writerow([0])

   
