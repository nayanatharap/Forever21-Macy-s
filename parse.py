import bs4 as bs
from urllib.request import Request, urlopen

import json, os

import subprocess

from lxml import etree

def main(product_link, output_path="./data", massive_json={}):

    req = Request(product_link, headers={'User-Agent': 'Mozilla/5.0'})
    sauce = urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, "lxml")


#test code
    final_object = {}
    data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
#extract name of item
    name = data['itemListElement'][0]['name']

#extract urls of imgs
    image=data['itemListElement'][0]['image']
    image_list=image.split(",")
    for url in image_list
         if url.get('class') is not None and 'og:image' in url.get('class'):
            processed_link = "https:" + "/".join(url.get("href").split("/")[:16] + ["1920"] + url.get("href").split("/")[17:]).split("?")[0]

            file_output = os.path.join(output_path, processed_link.split("/")[-1])
            image_list.append({"filename":processed_link.split("/")[-1], "id":image_count, "url":processed_link})
            image_count += 1

            subprocess.run(["wget","-O",file_output,processed_link])
    assert len(image_list) > 0
    shared_id = image_list[-1]["filename"].split("_")[0]

    if shared_id in massive_json:
        first_download_of_item = False
        return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
    else:
        first_download_of_item = True

    final_object['images'] = image_list
    final_object["info"] = {'year': 2018, "description": "ZARA Dataset", 'id':shared_id, "product_url": product_link}

#extract description and composition
detail=data['itemListElement'][0]['description']

 #For loop to separate materials from description
 for x in range (0,len(detail.text)):
     if x != 'Content':
        description.append(detail.text[x])
     else:
        index=x+3
        break
        #For loop to separate composition from description
 for x in range (index,len(detail.text)):
    if x!= 'Size':
        composition_string.append(detail.text[x])
    else:
        break

#figure out how to get composition and composition_string from this
#Shell: 96% cotton, 4% spandex - Lining & Other contents: 100% polyester 

json_object=json.loads(soup)


#color
try: 
    color=json_object["Variants"][0]["ColorName"]








    # Image Download
    image_list = []
    image_count = 1
    for url in soup.find_all("a"):
        if url.get('class') is not None and 'og:image' in url.get('class'):
            processed_link = "https:" + "/".join(url.get("href").split("/")[:16] + ["1920"] + url.get("href").split("/")[17:]).split("?")[0]

            file_output = os.path.join(output_path, processed_link.split("/")[-1])
            image_list.append({"filename":processed_link.split("/")[-1], "id":image_count, "url":processed_link})
            image_count += 1

            subprocess.run(["wget","-O",file_output,processed_link])

    assert len(image_list) > 0
    shared_id = image_list[-1]["filename"].split("_")[0]

    if shared_id in massive_json:
        first_download_of_item = False
        return massive_json[shared_id], massive_json[shared_id]['info']['id'], first_download_of_item
    else:
        first_download_of_item = True

    final_object['images'] = image_list
    final_object["info"] = {'year': 2018, "description": "ZARA Dataset", 'id':shared_id, "product_url": product_link}

    # Composition and Price
    composition = []
    composition_string = []
    price = None
    json_object = None
    for script in soup.find_all('script', {'type': "text/javascript"}):
        if "material" in script.text:
            try:
                json_object = json.loads(script.text.split(" = ")[2].rstrip(';window.zara.viewPayload'))
                for detailed_composition_part in json_object["product"]['detail']['detailedComposition']['parts']:

                    composition.append(detailed_composition_part['description'])
                    composition.extend(detailed_composition_part['components'])
                    composition_string.append(detailed_composition_part['description'])

                    if len(detailed_composition_part['components']) != 0:
                        for parts in detailed_composition_part['components']:
                            composition_string.append(parts["material"])
                    else:
                        for area in detailed_composition_part['areas']:
                            composition.append(area['description'])
                            composition.extend(area['components'])
                            composition_string.append(area['description'])

                            for parts in area['components']:
                                composition_string.append(parts["material"])

                price = json_object["product"]['price']
            except Exception as e:
                print("Failed to parse correct text/javascript segment", e)

            break
    composition_string = " ".join(composition_string)
    # Color
    try:
        color = json_object["product"]['detail']['colors'][0]["name"]
    except Exception as e:
        print("Failed to parse json_object from text/javascript segment for color", e)

        find_color_instances = soup.find_all("p", {"class":"color"})
        assert len(find_color_instances) < 2

        color = find_color_instances[0].find("span", {"class": "_colorName"}).text

    # Title
    try:
        title = json_object["og:description"]['content']
    except Exception as e:
        print("Failed to parse json_object from text/javascript segment for title", e)

        title_instances = soup.find_all("h1", {"id": "h1Title"})
        assert len(title_instances) < 2
        title = title_instances[0].text

    # Description
   
    # try:
    #     description = json_object["product"]['description'].split("\n\n")[0]
    # except Exception as e:
    #     print("Failed to parse json_object from text/javascript segment for description", e)

        title_instances = soup.find_all("script", {"type": "application/ld+json"})
        # assert len(title_instances) < 2
        # # Can be improved by filtering height of model
        # title = title_instances[0].text
        detail=title_instances["description"]

        #For loop to separate materials from description
        for x in range (0,len(detail.text)):
            if x != 'Content':
                description.append(detail.text[x])
            else:
                index=x+3
                break
        #For loop to separate composition from description
        for x in range (index,len(detail.text)):
            if x!= 'Size':
                composition_string.append(detail.text[x])
            else:
                break


    categories = []
    for p in soup.find_all("p", {"a":"title"}):
        categories.append(p.text)

    final_object["annotation"] = {"categories": categories, "title": title, "color": color, "price": price,
                                  "description": description, "content": composition, "composition_string": composition_string}

    return final_object, final_object['info']['id'], first_download_of_item


if __name__ == '__main__':
    a,b, _ = main('https://www.zara.com/us/en/mini-golden-bowling-bag-p11366304.html?v1=5699536&v2=358020')
    print("done")