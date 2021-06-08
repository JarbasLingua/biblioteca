import nltk

META = {
    "corpus_id": "cess_cat_universal",
    "version": "0.1",
    "lang": "ca",
    "license": "",
    "format": "text"
}

nltk.download('cess_cat')


# EAGLES
# http://www.ilc.cnr.it/EAGLES96/annotate/annotate.html


def convert_to_universal_tag(t):
    tagdict = {
        'X': 'X',
        'Y': 'X',
        'i': 'X',
        'w': 'NOUN'  # time
    }
    t = t.lower().strip()
    if t.startswith("v"):
        return 'VERB'
    if t.startswith("p"):
        return 'PRON'
    if t.startswith("n"):
        return 'NOUN'
    if t.startswith("d"):
        return 'DET'
    if t.startswith("a"):
        return 'ADJ'
    if t.startswith("z"):
        return 'NUM'
    if t.startswith("s"):
        return 'ADP'
    if t.startswith("r"):
        return 'ADV'
    if t.startswith("c"):
        return 'CONJ'
    if t.startswith("f"):
        return '.'
    return tagdict.get(t)


with open(META["corpus_id"] + ".txt", "w") as f:
    for sent in nltk.corpus.cess_cat.tagged_sents():
        for (w, t) in sent:
            if w in ["-Fpa-", "-Fpt-"]:
                continue
            t = convert_to_universal_tag(t)
            f.write(w + "\t" + t + "\n")
        f.write("\n")
