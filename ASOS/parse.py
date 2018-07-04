import bs4 as bs
from urllib.request import Request, urlopen
import json, os
import requests
import subprocess

product_link = "http://us.asos.com/asos/asos-design-scuba-asymmetric-ruffle-front-midi-dress/prd/9248481?clr=pink&SearchQuery=&cid=5235&gridcolumn=1&gridrow=1&gridsize=4&pge=1&pgesize=72&totalstyles=9751"
output_path="./data"
massive_json={}
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
req = requests.get(product_link, headers=headers)
sauce = urlopen(req).read()
soup = bs.BeautifulSoup(sauce, "lxml")
final_object = {}

composition = ""
composition_string = []
material = ""
material_list = []
materials = "Materials: "
check = None
try:
    try:
        check = soup.find_all("h4","ABOUT ME", "span", "br")
    except Exception:
        check = soup.find_all("h4","ABOUT ME", "span")
except Exception:
        composition = "N/A" 
        composition_string = "N/A"

for item in check:
    try:   
        material += item.text
        try:
            material_list = material.split(", ")
        except Exception:
            material_list.append(material)

        for elem in material_list:
            try:
                elem.split(": ")[1]
            except Exception:
                pass
        for elem in material_list:
            materials += elem.split("% ")[1]
            composition += elem.split("% ")[0] + "%"
        composition_string = [materials, "Composition: " + composition]

    except Exception:
        composition = "N/A" 
print(composition)
print(composition_string)

if __name__ == '__main__':
    print("done")
