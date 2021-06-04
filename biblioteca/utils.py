import logging
from os import listdir
from os.path import join, isfile, dirname, isdir
import json
import requests
from biblioteca.corpora import *
from xdg import BaseDirectory as XDG


LOG = logging.getLogger("JarbasBiblioteca")
LOG.setLevel("INFO")

RESOURCE_DIR = join(dirname(__file__), "res")
CORPUS_IDS = []
CORPUS_META = {}
for f in listdir(RESOURCE_DIR):
    if not f.endswith(".json"):
        continue
    c = f.replace(".json", "")
    CORPUS_IDS.append(c)
    with open(join(RESOURCE_DIR, f)) as fi:
        CORPUS_META[c] = json.load(fi)


CORPUS2CLASS = {
    "yesnoquestions_V0.1": YesNoQuestions,
    "metal_songs": MetalSongs,
    "metal_bands": MetalBands,
    "metal_lyrics": MetalLyrics
}

_BASE_URL = "https://github.com/OpenJarbas/biblioteca/releases/download"
_VERSION = "0.0.1a1"
CORPUS2URL = {corpus_id: _BASE_URL + f"/{_VERSION}/{corpus_id}"
              for corpus_id in CORPUS_IDS}


def download(corpus_id, force=False):
    if corpus_id in CORPUS_IDS:
        url = CORPUS2URL[corpus_id]
    else:
        raise ValueError("invalid corpus_id")
    path = join(XDG.save_data_path("JarbasBiblioteca"), corpus_id + ".tar.gz")
    if isfile(path) and not force:
        LOG.info("Already downloaded " + corpus_id)
        return
    LOG.info("downloading " + corpus_id)
    LOG.info(url)
    LOG.info("this might take a while...")
    with open(path, "wb") as f:
        f.write(requests.get(url).content)
    # TODO extract .tar.gz to folder
    base_folder = join(XDG.save_data_path("JarbasBiblioteca"), corpus_id)


def load_corpus(corpus_id):
    if corpus_id not in CORPUS_META:
        raise ValueError("unknown corpus_id")

    base_folder = join(XDG.save_data_path("JarbasBiblioteca"), corpus_id)

    # dedicated class for this corpus
    if corpus_id in CORPUS2CLASS:
        return CORPUS2CLASS[corpus_id]()

    fmt = CORPUS_META[corpus_id]["format"]

    LOG.debug("loading: " + base_folder)

    if fmt == "text":
        return TextCorpusReader(c)
    elif fmt == "json":
        return JsonCorpusReader(c)
    return AbstractCorpusReader(c)

