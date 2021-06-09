import requests

url = "https://www.linguateca.pt/Repositorio/MemoriasTraducao/"

content = requests.get(url).text
for p in content.split("href=")[1:]:
    p = p.split(">")[0][1:-1]
    if "/" in p:
        continue
    file_url = url + p
    with open(p, "w") as f:
        f.write(requests.get(file_url).text)
