import nltk

def extractTokens(text):
    return nltk.word_tokenize(text)

def getPosTag(tokens):
    return nltk.pos_tag(tokens)

def lemmatizeWithPOS(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    pos_tuples = getPosTag(tokens)
    lemma_list = []
    for (token, pos_tag) in pos_tuples:
        lemma_list.append(lemmatizer.lemmatize(token), pos=pos_tag)
    return lemma_list

def lemmatizeWithoutPOS(tokens):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma_list = []
    for token in tokens:
        lemma_list.append(lemmatizer.lemmatize(token))
    return lemma_list

def lemmatizePosTuple(pos_tuples):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma_list = []
    for (token, pos_tag) in pos_tuples:
        lemma_list.append(lemmatizer.lemmatize(token), pos=pos_tag)
    return lemma_list

def wordFrequency(tokens):
    return nltk.FreqDist(tokens)