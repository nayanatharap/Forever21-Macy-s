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
req = Request("https://www.forever21.com/us/shop/catalog/product/f21/women-new-arrivals/2000262551", headers={'User-Agent': 'Mozilla/5.0'})
sauce = urlopen(req).read()
soup = bs.BeautifulSoup(sauce, "lxml")


#Methods
def is_number(x):
    try:
        float(x)
        return True
    except (ValueError):
        return False



# #initialization of variables
detail=""
image=""
image_list=[]
image_count=0
title=""
price=""

for elem in soup.find_all("h1"):
    title=elem.text

#print out description of product
for elem in soup.find_all("script",{"type":"application/ld+json"}):
    json_object=json.loads(elem.text)
    image=json_object["image"]
    detail=json_object["description"]
    price=json_object["Offers"]["price"]
    

for link in image:
    processed_link = link

    file_output = os.path.join(output_path, str(image_count)+processed_link.split("/")[-1])
    image_list.append({"filename":str(image_count)+processed_link.split("/")[-1], "id":image_count, "url":processed_link})
    image_count+=1
    subprocess.run(["wget", "-O", file_output, processed_link])


description=""
composition_stringFull=""
composition_string=""
tempList=[]
tempCompList=[]
index=0


#separate description into composition, composition string and details

#Create details
words=detail.split("Content")
description=words[0]
wordsTwo=words[1].split("Care - ")
wordsTwo[1].replace("Machine","Hand")
wordsThree=wordsTwo[1].split("- Hand")
composition_stringFull=wordsThree[0]
print(description)
print(composition_string)
print(title)
print(price)


#Create composition_string
composition_stringFull=composition_stringFull.replace(" ","")
composition_List=composition_stringFull.split("-")
for num in range(0,len(composition_List)):
    composition_List[num]=composition_List[num].replace(":"," ")
    composition_List[num]=composition_List[num].replace("%"," ")
    composition_List[num]=composition_List[num].replace(","," ")
    for elem in composition_List[num].split(" "):
        tempList.append(elem)

for elem in tempList:
    if not is_number(elem):
        composition_string+=elem+" "

print (composition_string)
print (composition_stringFull)




# color=""


# for elem in soup.find_all("script",{"type":"text/javascript"}):
#     if "ColorName" in elem.text:
#         try:
#             json_object=json.loads(elem.text)
#             color=json_object["ColorName"]
#         except (ValueError):
#             print("Parse failed for color")