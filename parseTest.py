import bs4 as bs
from urllib.request import Request, urlopen

import json, os

import subprocess,time

import logging

from lxml import etree

exp_name = 'Forever21_' + time.time().__str__()
logging.basicConfig(filename=exp_name + ".log", level=logging.INFO)

output_path = "./" + exp_name + "_data"
os.makedirs(output_path, exist_ok=False)

#Obtaining information from webste to lxml form
req = Request("https://www.forever21.com/us/shop/Catalog/Product/f21/app-main/2000256354", headers={'User-Agent': 'Mozilla/5.0'})
sauce = urlopen(req).read()
soup = bs.BeautifulSoup(sauce, "lxml")

#initialization of variables
detail=""
image=""
image_list=[]
image_count=0
title=""

for elem in soup.find_all("h1"):
    title=elem.text

#print out description of product
for elem in soup.find_all("script",{"type":"application/ld+json"}):
    json_object=json.loads(elem.text)
    image=json_object["image"]
    detail=json_object["description"]
    

for link in image:
    processed_link = link

    file_output = os.path.join(output_path, str(image_count)+processed_link.split("/")[-1])
    image_list.append({"filename":str(image_count)+processed_link.split("/")[-1], "id":image_count, "url":processed_link})
    image_count+=1
    subprocess.run(["wget", "-O", file_output, processed_link])


description=""
composition_string=""
index=0
#separate description into composition, composition string and details
words=detail.split("Content")
description=words[0]
wordsTwo=words[1].split("Care - Shell:")
wordsTwo[1].replace("Machine","Hand")
wordsThree=wordsTwo[1].split("- Hand")
composition_string=wordsThree[0]
print(description)
print(composition_string)
print(title)


#print (description)
#print (composition_string)


# for elem in soup.find_all("script",{"type":"text/javascript"}):
#     json_object=json.loads(elem.text)
#     print("hlelo")
#     try:
#         color=json_object["ColorName"]
#         break;
#     except (TypeError):
#         pass