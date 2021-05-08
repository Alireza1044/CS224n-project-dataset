from nltk import sent_tokenize, word_tokenize
import preprocess
import utils
import statistics


def sentece_word_count(dialogs):
    print(f"dwight sentences: {len(sent_tokenize(' '.join(dialogs['dwight'])))}")
    print(f"michael sentences: {len(sent_tokenize(' '.join(dialogs['michael'])))}")
    print(f"dwight words: {len(word_tokenize(' '.join(dialogs['dwight'])))}")
    print(f"michael words: {len(word_tokenize(' '.join(dialogs['michael'])))}")


def character_stats(characters, dialogs):
    final_data = []
    for character in characters:
        output, total_sents, word_count = preprocess.remove_accent_and_expand(character, dialogs)
        final_data.append(output)
        print(f"total number of {character} sentences and words: {total_sents} , {word_count}")


def total_sents(data, characters):
    num = [sum([len(data[char]) for char in characters])]
    print(num[0])


def total_words(data, characters):
    words = sum([len(' '.join(data[char]).split()) for char in characters])
    distinct_words = sum([len(list(set(' '.join(data[char]).split()))) for char in characters])
    num = [sum([len(data[char]) for char in characters]), words, distinct_words]
    print(f"total number of words: {num[0]} and distinct words: {num[1]}")
    utils.plot(["sentences", "words", "distinct words"], num, "total word count")


def char_total_sents(data, characters):
    sentence_count = [len(data[c]) for c in characters]
    utils.plot(characters, sentence_count, "sentence count based on each character")


def distinct_words(data):
    michael_distinct = list(set(' '.join(data["michael"]).split()))
    dwight_distinct = list(set(' '.join(data["dwight"]).split()))
    both = 0
    only_michael = 0
    only_dwight = 0

    for word in michael_distinct:
        if word in dwight_distinct:
            both += 1
        else:
            only_michael += 1

    for word in dwight_distinct:
        if word not in michael_distinct:
            only_dwight += 1

    print(
        f"distinct words in both classes: {both} , first class only: {only_dwight} , second class only: {only_michael}")

    utils.plot(["both", "dwight", "michael"], [both, only_michael, only_dwight], "distinct words based on each group")


def most_repeated(data):
    michael_distinct_count = utils.word_count(' '.join(data["michael"]))
    dwight_distinct_count = utils.word_count(' '.join(data["dwight"]))
    michael_distinct_count = dict(sorted(michael_distinct_count.items(), key=lambda item: item[1], reverse=True))
    dwight_distinct_count = dict(sorted(dwight_distinct_count.items(), key=lambda item: item[1], reverse=True))

    dwight_most_repeated = []
    michael_most_repeated = []
    for word, count in michael_distinct_count.items():
        if word not in dwight_distinct_count.keys():
            michael_most_repeated.append((word, count))
        if len(michael_most_repeated) >= 10:
            break

    for word, count in dwight_distinct_count.items():
        if word not in michael_distinct_count.keys():
            dwight_most_repeated.append((word, count))
        if len(dwight_most_repeated) >= 10:
            break

    print(dwight_most_repeated)
    print(michael_most_repeated)
    utils.plot([x[0] for x in dwight_most_repeated], [x[1] for x in dwight_most_repeated], "Dwight", True)
    utils.plot([x[0] for x in michael_most_repeated], [x[1] for x in michael_most_repeated], "Michael", True)
    return dwight_most_repeated, michael_most_repeated


def x(data):
    word_frequency = utils.word_count(' '.join(data["michael"]) + ' '.join(data["dwight"]))

    word_frequency = dict(sorted(word_frequency.items(), key=lambda item: item[1], reverse=True))

    _ = [print(x) for x in list(word_frequency.items())[:10]]

    utils.plot(list(word_frequency.keys())[:180], list(word_frequency.values())[:180], "Histogram of Word Frequencies",
               True,
               True)


def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict


def computeIDF(documents):
    import math
    N = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict


def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def tfidf(data):
    documentA = ' '.join(data['michael'])
    documentB = ' '.join(data['dwight'])

    bagOfWordsA = documentA.split(' ')
    bagOfWordsB = documentB.split(' ')

    uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))

    numOfWordsA = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsA:
        numOfWordsA[word] += 1
    numOfWordsB = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsB:
        numOfWordsB[word] += 1

    tfA = computeTF(numOfWordsA, bagOfWordsA)
    tfB = computeTF(numOfWordsB, bagOfWordsB)

    idfs = computeIDF([numOfWordsA, numOfWordsB])

    tfidfA = computeTFIDF(tfA, idfs)
    tfidfB = computeTFIDF(tfB, idfs)

    return tfidfA, tfidfB, documentA, documentB


def plot_tfidf(df):
    tfidf_1 = {}
    tfidf_2 = {}
    for k in df.keys():
        tfidf_1[k] = df[k][0]
        tfidf_2[k] = df[k][1]

    tfidf_1 = dict(sorted(tfidf_1.items(), key=lambda item: item[1], reverse=True))
    tfidf_2 = dict(sorted(tfidf_2.items(), key=lambda item: item[1], reverse=True))

    _ = [print(item) for item in list(tfidf_1.items())[:10]]
    utils.plot(list(tfidf_1.keys())[:10], list(tfidf_1.values())[:10], "TF-IDF of Word Frequencies - Michael", True)

    _ = [print(item) for item in list(tfidf_2.items())[:10]]
    utils.plot(list(tfidf_2.keys())[:10], list(tfidf_2.values())[:10], "TF-IDF of Word Frequencies - Dwight", True)


def compute_RNF(docA, docB):
    wc_A = utils.word_count(docA)
    wc_B = utils.word_count(docB)
    total_A = sum([value for value in wc_A.values()])
    total_B = sum([value for value in wc_B.values()])

    RNF = {}

    for word in wc_A.keys():
        if word not in wc_B.keys():
            continue
        RNF[word] = (wc_A[word] / total_A) / (wc_B[word] / total_B)

    return dict(sorted(RNF.items(), key=lambda item: item[1], reverse=True))


def plot_RNF(documentA, documentB):
    RNF_A = statistics.compute_RNF(documentA, documentB)
    RNF_B = statistics.compute_RNF(documentB, documentA)

    _ = [print(item) for item in list(RNF_A.items())[:10]]
    utils.plot(list(RNF_A.keys())[:10], list(RNF_A.values())[:10], "RNF - Michael", True)

    _ = [print(item) for item in list(RNF_B.items())[:10]]
    utils.plot(list(RNF_B.keys())[:10], list(RNF_B.values())[:10], "RNF - Dwight", True)
