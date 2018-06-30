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
    for elem in soup.find_all("ul",{"class":"c-reset scroller swiper animated"}):
        for image in elem.find_all("meta",{"itemprop":"image"}):
            imagesList.append(image.get("content"))
        image_count = 1
        for url in imagesList:
            
            processed_link = url.split("wid")[0]+"wid=1230&hei=1500&fit=fit,1&$filterxlrg$"
            file_output = os.path.join(output_path, processed_link.split("/")[-1])
            image_list.append({"filename":processed_link.split("/")[-1], "id":image_count, "url":processed_link})
            image_count += 1

            subprocess.run(["wget", "-O", file_output, processed_link])
            subprocess.run(["wget", "-O", file_output, processed_link])
            im=Image.open(file_output)
            out=im.convert("RGB")
            out.save(file_output.split(".tif")[0]+".jpeg",quality=90)
            os.remove(file_output)

        assert len(image_list) > 0
        shared_id = image_list[-1]["filename"].split("_")[0]

        if shared_id in massive_json:
            first_download_of_item = False
            return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
        else:
            first_download_of_item = True

        final_object['images'] = image_list
        final_object["info"] = {'year': 2018, "description": "Macys Dataset", 'id':shared_id, "product_url": product_link}   
    print("Images Done")
    json_object = None
    json_object={}

    # Attributes
    attributes = []
    for item in soup.find_all("ul",{"data-auto":"product-description-bullets"}):
        for elem in item.find_all("li"):
            attributes.append(elem.text)
    print("Attributes Done")
    
    # Composition
    composition = ""
    listItems = []
    try:
        for x in range (0, 50):
            if "washable" in attributes[x]:
                listItems.append(attributes[x-1])
            elif "Dry" in attributes[x]:
                listItems.append(attributes[x-1])
            elif "clean" in attributes[x]:
                listItems.append(attributes[x-1])
            elif "wash" in attributes[x]:
                listItems.append(attributes[x-1])
            else:
                continue
    except IndexError:
        pass

    composition = listItems[0]
    print("Composition Done")
    
    # Price
    price1 = "Original: "
    price2 = "Sale: $"
    temp_price = ""
    sale_price = ""
    sale_value = []
    test = 0
    for script in soup.find_all("div", {"data-el":"price-details"}):
        if test == 0:
            try:
                for elem in script.find_all("div", {"class":"price", "data-auto":"main-price"}):
                    price1 += elem.text
                for elem in script.find_all("span", {"data-auto":"sale-price"}):
                    temp_price += elem.text
                sale_value = temp_price.split(" $")
                price2 += sale_value[1]
            except Exception:
                for elem in script.find_all("div", {"data-auto":"sale-price"}):
                    price1 += elem.text
                price2 = "No Sale"
            test=1
        else:
            break
    price = [price1.strip(), price2.strip()]
    print("Price Done")

    # Color
    color = ""
    for elem in soup.find_all("span", {"data-auto":"selected-color"}):
        color += elem.text
    print("Color Done")

    # Title and Brand
    title = ""
    for elem in soup.find_all("h1", {"data-auto":"product-name"}):
        title += elem.text
    title = title.strip()

    brand = ""
    for elem in soup.find_all("a", {"data-auto":"product-brand"}):
        brand+=elem.text
    brand = brand.strip()
    print("Title and Brand Done")

    # Description
    description = ""
    for elem in soup.find_all("p", {"data-auto":"product-description"}):
        description += elem.text
    description = description.strip()
    print("Description Done")

    # Categories
    categ = ""
    category_string = ""
    categories = []
    x = 0
    for elem in soup.find_all("title"):
        if(x==0):
            categ += elem.text
            x = 1
        else:
            pass
    
   
    category = []
    category = categ.split(" - ")
    categories = category[1:-1]
    categories = categories[::-1]
    print("Categories Done")

    final_object["annotation"] = {"categories": categories, "title": title, "brand": brand, "color": color, "price": price,
                                  "description": description, "composition": composition, "attributes": attributes}

    return final_object, final_object['info']['id'], first_download_of_item

if __name__ == '__main__':
    print("done")
