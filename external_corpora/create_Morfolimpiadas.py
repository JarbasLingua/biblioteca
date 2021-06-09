import requests

url = "https://www.linguateca.pt/aval_conjunta/morfolimpiadas/"

content = requests.get(url + "desc_textos_fig.html").text
for p in content.split("href=")[1:]:
    p = p.split(">")[0][1:-1]
    if "http" in p:
        continue
    if not p.endswith(".txt") and not p.endswith(".pdf"):
        continue
    file_url = url + p
    with open(p, "wb") as f:
        f.write(requests.get(file_url).content)
    print(file_url)
