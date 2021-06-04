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
    """ TODO """


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
