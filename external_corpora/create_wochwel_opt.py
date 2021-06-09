import requests
from os.path import join, dirname

url = "http://alfclul.clul.ul.pt/wochwel/"

content = requests.get(url + "oldtexts.html").text

for p in content.split("href=")[1:]:
    p = p.split('"')[1]

    if not p.endswith(".txt"):
        continue
    file_url = url + p

    with open(join(dirname(__file__), "wochwel_opt", p.split("/")[-1]),
              "w") as f:
        f.write(requests.get(file_url).text)
