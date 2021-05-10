import os
import nltk
import statistics
import crawl
import utils
import argparse
import pandas as pd


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--crawl', action='store_true',
                        help="Whether to crawl the raw data or not. default: False")

    parser.add_argument('-p', '--process', action='store_true',
                        help="Whether to clean and process the raw data or not. default: False")

    parser.add_argument('-s', '--stats', action='store_true',
                        help="Whether to report statistics of the data. default: False")
    return parser


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()

    path = os.path.join("data", "raw", "all_characters")
    if args.crawl:
        dialogs = crawl.crawl_data()
        utils.clean_path(path)
        path = os.path.join(path, "all_characters.json")
        utils.save_all_characters(dialogs, path)
        """# Saving raw data"""

    """# Clean up data"""
    if args.process:
        """## Save Michael and Dwight dialogues"""
        dialogs = utils.load_all_characters()
        path = os.path.join("data", "raw", "michael_dwight_dialogues")
        utils.clean_path(path)
        characters = ['michael', 'dwight']
        dialogs = {character: dialogs[character] for character in characters}
        print(len(dialogs['michael']), len(dialogs['dwight']))
        utils.save_characters_raw(dialogs)

        dialogs, _ = utils.load_cleaned(path)
        path = os.path.join("data", "clean")
        utils.clean_path(path)
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        characters = ["michael", "dwight"]
        statistics.character_stats(characters, dialogs)

    """# Statistics"""
    if args.stats:
        utils.clean_path(os.path.join('data', 'plots'))
        path = os.path.join('data', 'clean', 'cleaned_lemmatized_broken_sentences')
        data, characters = utils.load_cleaned(path)
        statistics.total_words(data, characters)
        statistics.char_total_sents(data, characters)
        statistics.distinct_words(data)
        statistics.total_sents(data, characters)
        statistics.most_repeated(data)
        statistics.word_frequency(data)
        tfidfA, tfidfB, documentA, documentB = statistics.tfidf(data)
        df = pd.DataFrame([tfidfA, tfidfB])
        statistics.plot_tfidf(df)
        statistics.plot_RNF(documentA, documentB)

    print("Finished running the script.")
