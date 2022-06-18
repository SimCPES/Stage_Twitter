"""Programme contenant la fonction de traitement du texte des tweets détaillée dans le rapport de stage"""

import nltk
import spacy
import string
from unidecode import unidecode

# On charge le modèle Spacy
nlp = spacy.load("fr_core_news_md")

# On récupère les comptes des candidats à l'élection
comptes = []
for line in open("./comptes.txt"):
    comptes.append(f"@{line[:-1].lower()}")

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
