import requests
from os.path import join, dirname

url = "http://corporavm.uni-koeln.de/colonia/"

content = requests.get(url + "inventory.html").text

for p in content.split("href=")[1:]:
    p = p.split(">")[0][1:-1]

    if not p.endswith(".txt"):
        continue
    file_url = url + p

    with open(join(dirname(__file__), "colonia_chp", p.split("/")[-1]),
              "w") as f:
        f.write(requests.get(file_url).text)
