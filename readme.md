# Biblioteca

```python
from biblioteca import load_corpus

corpus = load_corpus("metal_lyrics")
print(corpus.corpus_id)  # metal_lyrics
print(corpus.folder)  # ~/.local/share/JarbasBiblioteca/metal_lyrics
print(corpus.get_file_names())
for filename, lines in corpus.paragraphs(file_id="heavy_metal_lyrics.txt"):
    print(lines[-1])
    # I'll acquaint you with your shadow
    # I'll turn your day to night
    # The dark within will tear asunder
    # I've got your soul it's mine

```