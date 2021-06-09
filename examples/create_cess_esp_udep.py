import nltk
from biblioteca.utils.tagsets import eagles_to_udep
import json

META = {
    "corpus_id": "cess_esp_udep",
    "tagset": "Universal Dependencies",
    "tagset_homepage": "https://universaldependencies.org",
    "original_tagset": "EAGLES",
    "original_tagset_homepage": "http://www.ilc.cnr.it/EAGLES96/annotate/annotate.html",
    "version": "0.1",
    "lang": "es",
    "license": "",
    "format": "text"
}

nltk.download('cess_esp')
sentences = list(nltk.corpus.cess_esp.tagged_sents())

with open(META["corpus_id"] + ".txt", "w") as f:
    for sent in sentences:
        for (w, t) in sent:
            if w in ["-Fpa-", "-Fpt-"]:
                continue
            f.write(w + "\t" + eagles_to_udep(t) + "\n")
        f.write("\n")
META["num_entries"] = len(sentences)
with open(META["corpus_id"] + ".json", "w") as f:
    json.dump(META, f, indent=4)