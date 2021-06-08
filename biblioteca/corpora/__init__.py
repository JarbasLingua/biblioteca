import json
from os import listdir
from os.path import join

from quebra_frases import word_tokenize, sentence_tokenize, paragraph_tokenize
from xdg import BaseDirectory as XDG


class AbstractCorpusReader:
    def __init__(self, corpus_id, folder=None):
        self.corpus_id = corpus_id
        self.folder = folder or join(XDG.save_data_path("JarbasBiblioteca"),
                                     corpus_id)
        self.corpora = {}
        self.load()

    def raw(self, file_id=None):
        if file_id:
            return self.corpora.get(file_id)
        return self.corpora

    def get_files(self):
        return [join(self.folder, f) for f in self.get_file_names()]

    def get_file_names(self):
        return listdir(self.folder)

    def load(self):
        pass


class TextCorpusReader(AbstractCorpusReader):

    def load(self):
        for f in self.get_file_names():
            if not f.endswith(".txt"):
                continue
            with open(join(self.folder, f), errors='surrogateescape') as fi:
                self.corpora[f] = fi.read()

    def lines(self, file_id=None):
        if file_id:
            yield file_id, self.corpora[file_id].split("\n")
        else:
            for f in self.corpora:
                yield f, self.corpora[f].split("\n")

    def words(self, file_id=None):
        if file_id:
            yield file_id, set(word_tokenize(self.corpora[file_id]))
        else:
            for f in self.corpora:
                yield f, set(word_tokenize(self.corpora[f]))

    def sentences(self, file_id=None):
        if file_id:
            yield file_id, sentence_tokenize(self.corpora[file_id])
        else:
            for f in self.corpora:
                yield f, sentence_tokenize(self.corpora[f])

    def paragraphs(self, file_id=None):
        if file_id:
            yield file_id, paragraph_tokenize(self.corpora[file_id])
        else:
            for f in self.corpora:
                yield f, paragraph_tokenize(self.corpora[f])


class JsonCorpusReader(AbstractCorpusReader):
    def load(self):
        for f in self.get_file_names():
            if not f.endswith(".json"):
                continue
            with open(join(self.folder, f), errors='surrogateescape') as fi:
                self.corpora[f] = json.load(fi)

    def entries(self, key=None):
        if key:
            yield key, self.corpora[key]
        else:
            for k in self.corpora:
                yield k, self.corpora[k]

    def keys(self):
        return list(self.corpora.keys())


class JsonDbCorpusReader(JsonCorpusReader):
    """ json_database https://github.com/HelloChatterbox/json_database """

    def load(self):
        for f in self.get_file_names():
            if not f.endswith(".jsondb"):
                continue
            with open(join(self.folder, f), errors='surrogateescape') as fi:
                for db_name, json_data in json.load(fi).items():
                    self.corpora[db_name] = json_data

    def entries(self, db_name=None):
        for db, entries in self.corpora.items():
            if db_name and db != db_name:
                continue
            for e in entries:
                yield db_name, e

    def database_names(self):
        return self.keys()


class YesNoQuestions(TextCorpusReader):
    def __init__(self):
        super().__init__("yesnoquestions_V0.1")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalBands(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_bands")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalSongs(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_songs")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        for s in self.lines(file_id):
            yield s


class MetalLyrics(TextCorpusReader):
    def __init__(self):
        super().__init__("metal_lyrics")

    def sentences(self, file_id=None):
        for s in self.lines(file_id):
            yield s

    def paragraphs(self, file_id=None):
        if file_id:
            yield file_id, self.corpora[file_id].split("\n\n")
        else:
            for f in self.corpora:
                yield f, self.corpora[f].split("\n\n")


class TrveKvlt(JsonDbCorpusReader):
    def __init__(self):
        super().__init__("ytcat_trveKvlt")

    def entries(self, entry_id=None):
        for db_name, entries in self.corpora.items():
            for e in entries:
                eid = e.get("identifier")
                if not eid:
                    continue
                if entry_id:
                    if eid == entry_id:
                        yield db_name, e
                else:
                    yield eid, e

    def title(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["title"]

    def descriptions(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["description"]

    def tags(self, entry_id=None):
        for db_name, e in self.entries(entry_id):
            yield db_name, e["tags"] or []


class CessUniversal(TextCorpusReader):
    def load(self):
        self.corpora = []
        for f in self.get_file_names():
            if not f.endswith(".txt"):
                continue
            with open(join(self.folder, f), errors='surrogateescape') as fi:
                lines = fi.read().split("\n\n")
                for l in lines:
                    if not l:
                        continue
                    tagged_words = [tuple(w.split("\t"))
                                    for w in l.split("\n")]
                    self.corpora += [tagged_words]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for l in self.lines():
            for w in l:
                yield w[0]

    def sentences(self, *args, **kwargs):
        for l in self.lines():
            yield " ".join([w[0] for w in l])

    def paragraphs(self, *args, **kwargs):
        for l in self.sentences():
            yield l

    def tagged_words(self):
        for l in self.lines():
            for w in l:
                yield w

    def tagged_sentences(self):
        for l in self.lines():
            yield l


class CessCatUniversal(CessUniversal):
    def __init__(self):
        super().__init__("cess_cat_universal")


class CessEspUniversal(CessUniversal):
    def __init__(self):
        super().__init__("cess_esp_universal")
