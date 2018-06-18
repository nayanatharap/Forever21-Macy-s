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
        image_count = 1
        for url in imagesList:
            
            processed_link = url
            file_output = os.path.join(output_path, processed_link.split("/")[-1])
            image_list.append({"filename":processed_link.split("/")[-1], "id":image_count, "url":processed_link})
            image_count += 1

            subprocess.run(["wget", "-O", file_output, processed_link])

        assert len(image_list) > 0
        shared_id = image_list[-1]["filename"].split("_")[0]

        if shared_id in massive_json:
            first_download_of_item = False
            return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
        else:
            first_download_of_item = True

        final_object['images'] = image_list
        final_object["info"] = {'year': 2018, "description": "ZARA Dataset", 'id':shared_id, "product_url": product_link}   

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

    # Title and Brand
    title = json_object['name']
    brand = json_object['brand']["name"]

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

    final_object["annotation"] = {"categories": categories, "title": title, "brand": brand, "color": color, "price": price,
                                  "description": description, "content": composition, "attributes": attributes}

    return final_object, final_object['info']['id'], first_download_of_item


if __name__ == '__main__':
    a,b, _ = main('https://www.zara.com/us/en/mini-golden-bowling-bag-p11366304.html?v1=5699536&v2=358020')
    print("done")