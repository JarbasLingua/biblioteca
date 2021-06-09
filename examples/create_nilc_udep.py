from biblioteca.corpora.external import NILC
from biblioteca.utils.tagsets import nilc_to_udep
import json

META = {
    "corpus_id": "nilc_udep",
    "corpus_homepage": "http://www.nilc.icmc.usp.br/nilc/tools/nilctaggers.html",
    "tagset": "Universal Dependencies",
    "tagset_homepage": "https://universaldependencies.org",
    "original_tagset": "NILC_taggers",
    "original_tagset_homepage": "http://www.nilc.icmc.usp.br/nilc/download/tagsetcompleto.doc",
    "version": "0.1",
    "lang": "pt-br",
    "license": "",
    "format": "text"
}

corpus = NILC()
sentences = list(corpus.tagged_sentences())
with open(META["corpus_id"] + ".txt", "w") as f:
    for sent in sentences:
        for (w, t) in sent:
            f.write(w + "\t" + nilc_to_udep(t) + "\n")
        f.write("\n")
META["num_entries"] = len(sentences)
with open(META["corpus_id"] + ".json", "w") as f:
    json.dump(META, f, indent=4)