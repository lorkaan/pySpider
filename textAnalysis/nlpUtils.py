import nltk

'''

General Purpose preprocessing text functions that could be useful.

'''

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
        try:
            lemma_list.append(lemmatizer.lemmatize(token), pos=pos_tag)
        except:
            lemma_list.append(lemmatizer.lemmatize(token))
    return lemma_list

def wordFrequency(tokens):
    return nltk.FreqDist(tokens)

def getFreqDistFromLemmaPosTags(text):
    return wordFrequency(lemmatizePosTuple(getPosTag(extractTokens(text))))

def getMaxFreqDist(freqDist, num=0):
    return freqDist.most_common(num)

'''
Only good when you need to get the percent from a subset 
of the frequency distribution, where the subset is n max numbers
(n < N(), note: really should only be used to avoid time consuming decimal calculations)

GENERAL USE: USE getMaxPercentageFreqDist()

'''
def getPercentOnlyMaxFreqDist(freqDist, num=0):
    percentList = {}
    total = 0
    for word, num in freqDist.most_common(num):
        percentList[word] = num
        total = total + num
    total = 1.0 * total
    for k, v in percentList.items():
        percentList[k] = v / total
    return percentList

def getMaxPercentageFreqDist(freqDist, num=0):
    percentList = {}
    for word, num in freqDist.max_common(num):
        percentList[word] = freqDist.freq(word)
    return percentList

'''
Gets a dictionary of the most significant words, words above a threshold
in a given frequency distribution.

'''
def getSignificant(freqDist, threshold):
    if threshold == 0:
        return freqDist.most_common()
    if threshold < 0:
        threshold = abs(threshold)
    significant = {}
    for word, num in freqDist.most_common():
        if threshold < 1:
            # threshold is a positive number, but less than 1, indicating percentage
            sig = freqDist.freq(word)
        else:
            # threshold is a positive number greater than or equal to 1, indicating word count
            sig = num
        if sig >= threshold:
            significant[word] = num
        else:
            break
    return significant
        
            
        