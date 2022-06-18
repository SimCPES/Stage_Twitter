"""Programme réalisant l'entrainement d'un classifieur de tweets à partir des données d'entrainement stockées dans le fichier text_tweets_100000.json"""

import naya
import json
import nltk
import spacy
import pandas as pd
import numpy as np
import string
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# On charge le modèle Spacy
nlp = spacy.load("fr_core_news_md")

# On récupère les comptes des candidats à l'élection
comptes = []
for line in open("./comptes.txt"):
    comptes.append(f"@{line[:-1].lower()}")

# On charge les données à utiliser : les textes de 100 000 tweets
with open("./text_tweets_100000.json") as f:
    tweets = json.load(f)

# On crée l'ensemble contenant les stopwords et la fonction permettant de les retirer
french_stopwords = set(nltk.corpus.stopwords.words("french"))
# On ajoute aux stopwords les signes de ponctuation qui ne portent pas de sens
french_stopwords.update(string.punctuation)
french_stopwords.update(["\'", "\"", "``", "..."])
# On crée une fonction qui retire les stopwords d'une liste de mots
filtre_stopfr = lambda text : [token for token in text if token.lower() not in french_stopwords]

def preprocess_tweet(tweet):
    """Fonction pour traiter le texte des tweets"""
    try:
        text = nlp(tweet) # On applique le modèle Spacy au tweet
    except UnicodeEncodeError:
        text = nlp(unidecode(tweet))
    t = []
    hasht = False
    for token in text:
        if "http" not in token.lemma_: # Cela permet de ne pas conserver les liens hypertextes
            # On retire les mentions d'utilisateurs sauf si c'est un candidat qui est mentionné
            # On retire également les sauts à la ligne et les mots d'un seul caractère qui ne peuvent pas porter de sens
            if (token.lemma_[0] != "@" or (token.lemma_[0] == "@" and token.lemma_ in comptes)) and ("\n" not in token.lemma_) and len(token.lemma_) > 1:
                if hasht: # Le modèle sépare le # et le texte qui suit, on souhaite conserver les # donc on les réunit
                    t.append(unidecode(f"#{token.lemma_}"))
                    hasht = False
                else:
                    t.append(unidecode(token.lemma_))
            elif token.lemma_ == "#":
                hasht = True
    text = filtre_stopfr(t) # On retire les stopwords
   
    return text

# On crée les objets calculant la matrice des scores TF-IDF et réalisant la réduction de dimension
tf_idf = TfidfVectorizer(tokenizer=preprocess_tweet)
PCA = TruncatedSVD(n_components=100) # On souhaite conserver 100 colonnes sur la matrice finale
forest = RandomForestClassifier() # On crée le classifieur

# On calcule la représentation numérique des données en calculant les scores TF-IDF et en appliquant la PCA
X = PCA.fit_transform(tf_idf.fit_transform(tweets))
# On récupère les étiquettes correspondantes stockées dans le fichier "tweets.csv"
y = np.genfromtxt("tweets.csv", delimiter=",")

# On sépare les données en données d'apprentissage et de test et on entraine le classifieur
X_train, X_test, y_train, y_test = train_test_split(X, y)
forest.fit(X_train, y_train)

# On calcule le score du classifieur sur l'échantillon de test
print("Score : ", tree.score(X_test, y_test))
