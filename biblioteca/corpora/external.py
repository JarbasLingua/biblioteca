from os.path import join

from biblioteca.corpora import TextCorpusReader


class Aeiouado(TextCorpusReader):
    def __init__(self):
        super().__init__("aeiouado")

    def load(self):
        with open(join(self.folder, "aeiouado-ipa-01.csv"),
                  errors='surrogateescape') as fi:
            self.corpora = [l for l in fi.read().split("\n") if l.strip()]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for l in self.lines():
            yield l.split("\t")[0]

    def sentences(self, *args, **kwargs):
        return self.words()

    def paragraphs(self, *args, **kwargs):
        return self.sentences()

    def tagged_words(self):
        for l in self.lines():
            yield l.split("\t")

    def pronounciations(self):
        return {k: v for (k, v) in self.tagged_words()}


class NILC(TextCorpusReader):
    def __init__(self):
        super().__init__("NILC_taggers")

    def load(self):
        with open(join(self.folder, "corpus100.txt"),
                  encoding="latin1") as fi:
            self.corpora = [l for l in fi.read().split("\n") if l.strip()]

    def lines(self, *args, **kwargs):
        for f in self.corpora:
            yield f

    def words(self, *args, **kwargs):
        for tagged in self.tagged_sentences():
            for s in tagged:
                yield s[0]

    def sentences(self, *args, **kwargs):
        for tagged in self.tagged_sentences():
            yield " ".join(s[0] for s in tagged)

    def paragraphs(self, *args, **kwargs):
        return self.sentences()

    def tagged_sentences(self):
        for l in self.lines():
            tagged = []
            for word in l.split(" "):
                if not word:
                    continue
                w = word.split("_")[0]
                t = word[len(w) + 1:]
                tagged.append((w, t))
            yield tagged

    def tag_list(self):
        tags = []
        for tagged in self.tagged_sentences():
            for s in tagged:
                tags.append(s[1])
        return sorted(list(set(tags)))

    def tags(self):
        tags = {}
        for tagged in self.tagged_sentences():
            for s in tagged:
                if s[1] not in tags:
                    tags[s[1]] = []
                if s[0] not in tags[s[1]]:
                    tags[s[1]].append(s[0])
        return tags
