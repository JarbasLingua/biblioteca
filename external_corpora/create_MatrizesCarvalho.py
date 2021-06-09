import requests

url = "https://www.linguateca.pt/Repositorio/RecursosPaulaCarvalho/"

content = requests.get(url).text
for p in content.split("href=")[1:]:

    p = p.split('"')[1]
    file_url = p
    p = file_url.split("/")[-1]


    if not p.endswith(".txt") and not p.endswith(".pdf"):
        continue

    with open(p, "wb") as f:
        f.write(requests.get(file_url).content)

