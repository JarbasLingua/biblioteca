import requests
from os.path import join, dirname

url = "https://www.linguateca.pt/Repositorio/CorrOrtog/"

content = requests.get(url).text
for p in content.split("href=")[1:]:
    p = p.split(">")[0][1:-1]
    if "http" in p:
        continue
    if not p.endswith(".txt") and not p.endswith(".pdf"):
        continue
    file_url = url + p
    with open(join(dirname(__file__), "CorrOrtog", p), "w") as f:
        f.write(requests.get(file_url).text)

