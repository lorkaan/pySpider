
def calculateSquaredError(target, output):
    return (target - output) ** 2

'''
Represents a Word with a given weight, weights always represented as decimal.
'''
class WeightedWord:

    @staticmethod
    def calculateError(target, output):
        tWeight = 0
        oWeight = 0
        if target is WeightedWord:
            tWeight = target.weight
        if output is WeightedWord:
            oWeight = output.weight
        return calculateSquaredError(tWeight, oWeight)

    def __init__(self, word, weight):
        self.word = word
        self.weight = 1.0 * weight

    def __eq__(self, other):
        return self.word == other.word

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __ge__(self, other):
        return self.weight >= other.weight

    def __str__(self):
        return f"{self.word}: {self.weight}"

    def __add__(self, other):
        return self.weight + other.weight

'''
Represents as Document object.
'''
class Document:

    def __init__(self, source, ww_collection):
        self.source = source
        self.tags = ww_collection # some sort of collection

    def determineRelativity(self, weightedWords):
        errorScore = {}
        for wword in weightedWords:
            errorScore[wword.word] = WeightedWord.calculateError(wword, self.tags[wword.word])  # as long as the collection implements __getitem__(self, key)
        return errorScore
