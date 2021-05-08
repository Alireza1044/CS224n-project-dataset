import os
import shutil
import json
from glob import glob
import matplotlib.pyplot as plt


def clean_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)


def save_all_characters(dialogs):
    path = os.path.join("data", "raw", "all_characters", "all_characters.json")
    with open(path, "w") as f:
        json.dump(dialogs, f, sort_keys=True, indent=4)


def load_all_characters():
    path = os.path.join("data", "raw", "all_characters", "all_characters.json")
    with open(path, 'r') as f:
        dialogs = json.load(f)
    return dialogs


def save_characters_raw(dialogs):
    path = os.path.join("data", "raw", "michael_dwight_dialogues")
    for character, dialogues in dialogs.items():
        with open(os.path.join(path, f"{character}.txt"), "w") as txt_file:
            for dialogue in dialogues:
                txt_file.write(f"{dialogue}\n")


def save_cleaned(character, folder, sents):
    path = os.path.join("data", "clean", folder)
    try:
        os.makedirs(path)
    except:
        pass
    path = os.path.join(path, f"{character}.txt")
    with open(path, "w") as txt_file:
        for sent in sents:
            txt_file.write(f"{sent}\n")


def load_cleaned(path):
    data = {}
    characters = []
    for file in glob(os.path.join(path, '*.txt')):
        name = os.path.basename(file).split('.')[0]
        characters.append(name)
        with open(file, 'r') as f:
            data[name] = [sent.strip() for sent in f.readlines()]
    return data, characters


def plot(names, numerical_data, title, shift=False, is_large=False):
    if is_large:
        fig = plt.figure(figsize=(25, 25))
    else:
        fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    if shift:
        plt.xticks(rotation=90)
        ax.xaxis.set_tick_params(labelsize=10)
    ax.bar(names, numerical_data)
    plt.title(title)
    plt.show()


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts
