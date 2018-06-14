import bs4 as bs
from urllib.request import Request, urlopen

import json, os, sys
import requests
import subprocess,time

import logging

from lxml import etree

def main(product_link,output_path="./data",massive_json={}):
#Obtaining information from webste to lxml form
    req = Request(product_link, headers={'User-Agent': 'Mozilla/5.0'})
    sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, "lxml")

    final_object={}



#Methods
#Method used to check if a character is a number
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
    image_count=1
    title=""
    price=""

#Find title of item
    for elem in soup.find_all("h1"):
        title=elem.text

#Obtain images, details, and price of item
    for elem in soup.find_all("script",{"type":"application/ld+json"}):
        json_object=json.loads(elem.text)
        image=json_object["image"]
        detail=json_object["description"]
        price=json_object["Offers"]["price"]

#for each image, output into folder
    for link in image:
        processed_link = link

        file_output = os.path.join(output_path, str(image_count)+processed_link.split("/")[-1])
        image_list.append({"filename":str(image_count)+processed_link.split("/")[-1], "id":image_count, "url":processed_link})
        image_count+=1
        subprocess.run(["wget", "-O", file_output, processed_link])
    shared_id=image_list[-1]["filename"].split("_")[0]
    if shared_id in massive_json:
        first_download_of_item = False
        return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
    else:
        first_download_of_item = True

    final_object['images'] = image_list
    final_object["info"] = {'year': 2018, "description": "Forever21 Dataset", 'id':shared_id, "product_url": product_link}
#initialization of variables for composition and escription
    description=""
    composition_stringFull=""
    composition_string=""
    tempList=[]
    tempCompList=[]
    composition=[]
    index=0


#separate description into composition, composition string and details

#Create details
    words=detail.split("Content")
    description=words[0]
    wordsTwo=words[1].split("Care - ")
    wordsTwo[1].replace("Machine","Hand")
    wordsThree=wordsTwo[1].split("- Hand")
    composition_stringFull=wordsThree[0]


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

    tempoList=composition_string.split("Machine|Hand")
    composition_string=tempoList[0]

#Create composition list
    composition_stringFull=composition_stringFull.replace(":"," : ")
    composition_stringFull=composition_stringFull.replace(","," , ")
    composition_stringFull=composition_stringFull.replace("-"," - ")


    tempCompList=composition_stringFull.split(" ")



    for x in range (0,len(tempCompList)):
        if tempCompList[x] is ':':
            composition.append(tempCompList[x-1])
        elif is_number(tempCompList[x][0]):
            smallList=tempCompList[x].split("%")
            composition.append("Material:"+smallList[1]+" , " + "Percentage: "+ smallList[0])





#Obtain color
    color=[]
    tempColor=[]

    for elem in soup.find_all("script",{"type":"text/javascript"}):
        if "ColorName" in elem.text:
            try:
                tempColor=elem.text.split("var pData =")
                tempColor=tempColor[1].split("brand =")
                tempColor=tempColor[0].rsplit(";",1)
                text=tempColor[0]
                json_object = json.loads(text)
                for index in range (0,5):
                    try:
                        color.append(json_object["Variants"][index]["ColorName"])
                    except (IndexError):
                        break
            except (ValueError):
                print ("could not parse")

    categories=""
    for elem in soup.find_all("a",{"href":"/us/shop/catalog/category/f21/app-main"}):
        categories+=elem.text
    print (color)
    print(title)
    print(price)
    print(composition_string)
    print(composition)
    print(description)
    print(categories)

    final_object["annotation"] = {"categories": categories, "title": title, "color": color, "price": price,
                                  "description": description, "content": composition, "composition_string": composition_string}    

    return (final_object,final_object['info']['id'],first_download_of_item)
    # listParts=["women-new-arrivals","dress","bottoms","top_blouses","swimwear_all","outerwear_coats-and-jackets","bottom_jeans","intimates_loungewear","activewear","acc","shoes","sale_women"]
    # for parts in listParts:
#     link="/us/shop/catalog/category/f21/"+parts
#     for elem in soup.find_all("a",{"href":link},{"class":"block"}):
#         print(elem.text)

