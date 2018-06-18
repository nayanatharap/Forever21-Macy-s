import bs4 as bs
from urllib.request import Request, urlopen
import json, os
import requests
import subprocess


def main(product_link, output_path="./data", massive_json={}):

    req = Request(product_link, headers={'User-Agent': 'Mozilla/5.0'})
    sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, "lxml")

    final_object = {}

    # Image Download
    imagesList=[]
    for index in range (0,5):
        try:
            for elem in soup.find_all("li",{"class":"main-image swiper-slide","data-index":index}):
                for image in elem.find_all("img"):
                    if index==0:
                        imagesList.append(image.get("src"))
                    else:
                        imagesList.append(image.get("data-src"))
        except IndexError:
            break

    json_object = None
    json_object={}

    # Composition
    composition = []

    for item in soup.find_all("ul",{"data-auto":"product-description-bullets"}):
        for elem in item.find_all("li"):
            listItems.append(elem.text)

    for x in range (0, len(listItems)):
        if "washable" in listItems[x]:
            composition=listItems[x-1]
        else:
            continue

    # Price
    price = None
    for script in soup.find_all('script', {'type': "application/ld+json"}):`
        json_object=json.loads(script.text)
        price = json_object["offers"][0]['price']
   
    # Attributes
    attributes = []
    for item in soup.find_all("ul",{"data-auto":"product-description-bullets"}):
        for elem in item.find_all("li"):
            attributes.append(elem.text)

    # Color
    color = []
    for x in range(0,10):
        try:
            color.append(json_object["offers"][x]["itemOffered"]["color"])
        except IndexError as e:
            break

    # Title
    title = json_object['name']

    # Description
    description = json_objec['description']

    # Categories
    categories = ""
    name = []
    newname = []
    
    for item in soup.find_all("title"):
        name = item.text.split(title)
        newname = name[1].split("- Macy's")

    categories = newname[0]

    final_object["annotation"] = {"categories": categories, "title": title, "color": color, "price": price,
                                  "description": description, "content": composition, "attributes": attributes}

    return final_object, final_object['info']['id'], first_download_of_item


if __name__ == '__main__':
    a,b, _ = main('https://www.zara.com/us/en/mini-golden-bowling-bag-p11366304.html?v1=5699536&v2=358020')
    print("done")