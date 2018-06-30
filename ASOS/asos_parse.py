import bs4 as bs
from urllib.request import Request, urlopen
import json, os
import requests
import subprocess

def main(product_link, output_path="./data", massive_json={}):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    req = requests.get(product_link, headers=headers)
    sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    final_object = {}

    # Image Download
    image_list=[]
    for index in range (0,5):
        try:
            for elem in soup.find_all("li",{"class":"main-image swiper-slide","data-index":index}):
                for image in elem.find_all("img"):
                    if index==0:
                        image_list.append(image.get("src"))
                    else:
                        image_list.append(image.get("data-src"))
        except IndexError:
            break
        image_count = 1
        for url in image_list:
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
        final_object["info"] = {'year': 2018, "description": "ASOS Dataset", 'id':shared_id, "product_url": product_link}   

    json_object = None
    json_object={}

    # Composition
    composition = None
    material = []
    for item in soup.find_all("h4","ABOUT ME", "span"):
        try:   
            name = item.text.split("main")
            composition = name[1]
            temp = composition
            for x in composition:
                if x=="%":
                    temp1 = temp.text.split(",")
                    temp2 = temp1[0].text.split("%")
                    material.append(temp2[1])
                    temp = temp[1]
        except Exception:
            composition = "N/A" 

    # Composition String
    composition_string = []
    temp = composition
    try:
        for x in composition:
            if x==",":
                composition_string.append(temp.text.split(","))
                temp = temp[1]

    # Price
    price = None
    for script in soup.find_all('script', {'type': "text/javascript"}):
        json_object=json.loads(script.text)
        price = json_object["price"][0]['current']

    # Color
    itemcolor = None
    color = []
    for x in range(0,10):
        try:
            for script in soup.find_all('script', {'type': "text/javascript"}):
                json_object=json.loads(script.text)
                itemcolor = json_object["images"][x]['colour']
            color.append(itemcolor)
        except IndexError:
            break

    # Title
    title_instances = soup.find_all("span", {"itemprop":"name"})
    assert len(title_instances) < 2
    title = title_instances[0].text

    # Description
    detail = []

    for item in soup.find_all({"class":"product-decription"}, "h4", "ul"):
        for elem in item.find_all("li"):
            detail.append(elem.text)

    # Categories
    categories = ""
    name = []
    x = 0
    for item in soup.find_all("breadcrumb:"):
        if (x==1):
            name = item.text.split(title)
        else:
            x = 1

    categories = name[0]

    final_object["annotation"] = {"categories": categories, "title": title, "color": color, "price": price,
                                  "description": detail, "content": composition}

    return final_object, final_object['info']['id'], first_download_of_item

if __name__ == '__main__':
    print("done")
