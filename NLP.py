"""Programme contenant la fonction de traitement du texte des tweets présentée dans le rapport de stage"""

import nltk  # Le module nltk permet d'avoir une liste de stopwords en français
import spacy   # On utilise un modèle du module Spacy adapté au français pour réaliser les opérations de lemmatisation
import string
from unidecode import unidecode   # Cette fonction permet de retirer les accents et caractères spéciaux qui ne peuvent pas être traités

# On charge le modèle Spacy
# Ce modèle est adapté au traitement de texte au français : https://spacy.io/models/fr 
nlp = spacy.load("fr_core_news_md")

# On récupère les comptes des candidats à l'élection
comptes = []
for line in open("./comptes.txt"):
    comptes.append(f"@{line[:-1].lower()}")

# On crée l'ensemble contenant les stopwords et la fonction permettant de les retirer à partir de la liste proposée par NLTK
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
        # 'token' représente un terme du tweet, 'token.lemma_' donne la forme lemmatisée de 'token' c'est à dire la forme canonique
        # du terme. On décide ensuite si on souhaite conserver ce terme ou pas.
        if "http" not in token.lemma_: # Cela permet de ne pas conserver les liens hypertextes
            # On retire les mentions d'utilisateurs sauf si c'est un candidat qui est mentionné
            # On retire également les sauts à la ligne et les mots d'un seul caractère qui ne peuvent pas porter de sens
            if (token.lemma_[0] != "@" or (token.lemma_[0] == "@" and token.lemma_ in comptes)) and ("\n" not in token.lemma_) and len(token.lemma_) > 1:
                if hasht: # Le modèle sépare le # et le texte qui suit en deux token, par exemple : '#presidentielle2022' donne '#' puis 'presidentielle2022'
                    # On souhaite conserver le fait qu'il s'agit d'un hashtag donc on les réunit
                    t.append(unidecode(f"#{token.lemma_}"))
                    hasht = False
                else:
                    t.append(unidecode(token.lemma_))
            elif token.lemma_ == "#":
                hasht = True
    text = filtre_stopfr(t) # On retire les stopwords
   
    return text
