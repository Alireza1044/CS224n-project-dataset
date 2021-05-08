import contractions
import unidecode
import utils
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


def remove_accented_chars(text):
    text = unidecode.unidecode(text)
    return text


def expand_contractions(text):
    text = contractions.fix(text)
    return text


def export_sentences(character, dialogs):
    return sent_tokenize(' '.join(dialogs[character]).lower())


def remove_accent_and_expand(character, dialogs):
    global lemmatizer
    sents = export_sentences(character, dialogs)
    sents_expanded = [expand_contractions(remove_accented_chars(sent)) for sent in sents]
    utils.save_cleaned(character, "cleaned_broken_sentences", sents_expanded)
    sents_lemmatized = []
    word_count = 0
    for sent in sents_expanded:
        sent_tokenized = word_tokenize(sent)
        if len(sent_tokenized) < 5:
            continue
        word_count += len(sent_tokenized)
        sents_lemmatized.append(' '.join([lemmatizer.lemmatize(word) for word in sent_tokenized]))
    utils.save_cleaned(character, "cleaned_lemmatized_broken_sentences", sents_lemmatized)
    return sents_lemmatized, len(sents_lemmatized), word_count
