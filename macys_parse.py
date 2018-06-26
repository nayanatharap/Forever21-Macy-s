import bs4 as bs
from urllib.request import Request, urlopen
import json, os
import requests
import subprocess
from PIL import Image

def main(product_link, output_path="./data", massive_json={}):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    req = requests.get(product_link, headers=headers)
    sauce = req.text
    soup = bs.BeautifulSoup(sauce, "lxml")
    final_object = {}

    # Image Download
    imagesList=[]
    image_list=[]
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

        for image in image_list:
            if image[-3:] == "tif":
                newimage = image[:-3] + "jpeg"
            try:
                im = Image.open(image)
                out = im.convert("RGB")
                out.save(newimage, "JPEG", quality=100)
            except Exception, e:
                print e
            images.append(out)
        

        assert len(image_list) > 0
        shared_id = image_list[-1]["filename"].split("_")[0]

        if shared_id in massive_json:
            first_download_of_item = False
            return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
        else:
            first_download_of_item = True

        final_object['images'] = image_list
        final_object["info"] = {'year': 2018, "description": "Macy's Dataset", 'id':shared_id, "product_url": product_link}   

    json_object = None
    json_object={}

    # Composition
    composition = []
    listItems = []
    for item in soup.find_all("ul",{"data-auto":"product-description-bullets"}):
        for elem in item.find_all("li"):
            listItems.append(elem.text)

    for x in range (0, len(listItems)):
        if "washable" in listItems[x]:
            composition=listItems[x-1]
        else if "Dry Clean" in listItems[x]:
            composition=listItems[x-1]
        else:
            continue

    # Price
    price = []
    for script in soup.find_all("div", {"data-el":"price-details"}):
        x = 0
        for value in script.find_all("$"):
            if(x==0):
                price[0] = "Original:" + value
                x = 1
            else:
                continue
        try:
            for value in script.find_all("Sale  $"):
                price[1] = "Sale: " + value
        except Exception:
            price[1] = "No Sale"
  
    # Attributes
    attributes = []
    for item in soup.find_all("ul",{"data-auto":"product-description-bullets"}):
        for elem in item.find_all("li"):
            attributes.append(elem.text)

    # Color
    color = None
    color = soup.find_all("Color:", "span", {"data-auto":"selected-color"})

    # Title and Brand
    title = json_object['name']
    try:
        new_title = item.text.split(", Created for Macy's")
        title = new_title[0]
    except Exception:
        break

    brand = json_object['brand']["name"]

    # Description
    description = json_object['description']

    # Categories
    categories = ""
    name = []
    newname = []
    temp_name = []
    category_string = []
    temp_categ = []
    
    for item in soup.find_all("title"):
        name = item.text.split(title)
        newname = name[1].split("- Macy's")
        temp_name = newname[0].split("- ")

    categories = temp_name[1]
    counter = 0
    for x in rage(0, len(categories)):
        if categories[x]=="-":
            counter = counter+1

    for item in range(0,counter):
        temp_categ = categories.text.split(" - ")
        category_string.append(temp_categ[0])
        categories = categories[1]

    category_string[::-1]


    final_object["annotation"] = {"categories": category_string, "title": title, "brand": brand, "color": color, "price": price,
                                  "description": description, "content": composition, "attributes": attributes}

    return final_object, final_object['info']['id'], first_download_of_item

if __name__ == '__main__':
    print("done")