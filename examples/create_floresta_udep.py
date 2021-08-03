from biblioteca.corpora.external import FlorestaCP
from biblioteca.utils.tagsets import floresta_to_udep
from biblioteca import download
import json

download("FlorestaVirgem_CF_3.0")
download("FlorestaVirgem_CP_3.0")

META = {
    "corpus_id": "floresta_udep",
    "corpus_homepage": "http://www.floresta.icmc.usp.br/floresta/tools"
                       "/florestataggers"
                       ".html",
    "tagset": "Universal Dependencies",
    "tagset_homepage": "https://universaldependencies.org",
    "original_tagset": "NILC_taggers",
    "original_tagset_homepage":
        "http://www.floresta.icmc.usp.br/floresta/download/tagsetcompleto.doc",
    "version": "0.1",
    "lang": "pt-br",
    "license": "",
    "format": "text"
}

corpus = FlorestaCP()
sentences = list(corpus.tagged_sentences())
print(sentences)
exit()
with open(META["corpus_id"] + ".txt", "w") as f:
    for sent in sentences:
        for (w, t) in sent:
            f.write(w + "\t" + floresta_to_udep(t) + "\n")
        f.write("\n")
META["num_entries"] = len(sentences)
with open(META["corpus_id"] + ".json", "w") as f:
    json.dump(META, f, indent=4)