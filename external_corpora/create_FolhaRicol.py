import requests
from os.path import join, dirname

url = "https://www.linguateca.pt/Repositorio/Folha-RIcol/"

content = requests.get(url).text

for p in content.split("href=")[1:]:
    p = p.split(">")[0][1:-1]
    if not p.endswith(".txt"):
        continue
    file_url = url + p
    with open(join(dirname(__file__), "FolhaRIcol", p), "w") as f:
        f.write(requests.get(file_url).text)

for p in content.split("HREF=")[1:]:
    p = p.split(">")[0][1:-1]
    if not p.endswith(".tgz"):
        continue
    file_url = url + p
    with open(join(dirname(__file__), "FolhaRIcol", p), "wb") as f:
        f.write(requests.get(file_url).content)

