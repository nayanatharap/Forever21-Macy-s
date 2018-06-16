import bs4 as bs
from urllib.request import Request, urlopen

import parseTemp, json

import pandas as pd

import tqdm, time, os

import logging

exp_name = 'Forever21_' + time.time().__str__()
logging.basicConfig(filename=exp_name + ".log", level=logging.INFO)

output_path = "./" + exp_name + "_data"
os.makedirs(output_path, exist_ok=False)

# Make the url call for the links
req = Request("https://www.forever21.com/us/shop", headers={'User-Agent': 'Mozilla/5.0'})
sauce = urlopen(req).read()
soup = bs.BeautifulSoup(sauce, "lxml")

# Hard coded filtering for woman products
woman_product_type_list = list(filter(lambda x: "women" in x[0] , [(k.get("href"), k.text)
                                                                                   for k in soup.find_all("a", {"class": "block"})]))
view_all_list = set(t[0] for t in filter(lambda x: x[1].lower() == "view all", woman_product_type_list))
woman_product_type_set = set([k[0] for k in woman_product_type_list]) - view_all_list

# Variable initializations
total_items_need, items_downloaded, num_multiple_category_items = 1000000, 0, 0
massive_json = {}
color, title, description, content, url_list = [], [], [], [], []


#ensure all elements of woman_product_type_set are full links
for elem in woman_product_type_set:
   # print("https://www.forever21.com"+elem)
    if (elem[0] is '/'):
        woman_product_type_set.add("https://www.forever21.com"+elem)
        woman_product_type_set.remove(elem)



final_object={}
json_object={}
listItems=[]

for product_type_link in tqdm.tqdm(woman_product_type_set):

    soup_product_type_page = bs.BeautifulSoup(urlopen(Request(product_type_link, headers={'User-Agent': 'Mozilla/5.0'})).read(), "lxml")
#Only search through text if it contains url
    for item in soup_product_type_page.find_all("script", {'type':"text/javascript"}):
        if not "ProductShareLinkUrl" in item.text:
            continue
        elif "ProductShareLinkUrl" in item.text:
            tempList=item.text.split("CatalogProducts")
            tempList=tempList[1].split("CategoryCustomerNote")
            tempList=tempList[0].rsplit("],",1)

#parse through elements of list

            tempList2=tempList[0].split("BackorderedQuantity")
            tempList2[0]=tempList2[0][3:]
#Check this line, messes up the first product link
            tempList2.remove(tempList2[0])

            for elem in tempList2:
                try:
#Obtain the url from each item
                    tempList3=elem.rsplit(",{",1)
                    elem='{"BackorderedQuantity'+tempList3[0]

                    json_object=json.loads(elem)
                    listItems.append(json_object["ProductShareLinkUrl"])
                except(ValueError):
                    continue

#Iterate through links in listItems
        for product_link in listItems:
            try:
                final_object, id, first_download_of_item = parseTemp.main(product_link, output_path, massive_json)
                if not first_download_of_item:
                    num_multiple_category_items += 1
                    print("Item_clash_for", id)
                    continue
            except Exception as e:
                print("Parse failed with ", e)
                

            massive_json[id] = final_object

            color.append(final_object["annotation"]["color"])
            title.append(final_object["annotation"]["title"])
            description.append(final_object["annotation"]["description"])
            content.append(final_object["annotation"]["composition_string"])
            url_list.append(final_object['info']['product_url'])
            items_downloaded += 1

            print("items_downloaded", items_downloaded)
            if items_downloaded > total_items_need:
                break

    json.dump(massive_json, open(exp_name + "_details.json", "w"))

    data_frame = pd.DataFrame()
    data_frame["color"] = color
    data_frame['title'] = title
    data_frame['description'] = description
    data_frame["content"] = content
    data_frame["url_list"] = url_list

    data_frame.to_excel(exp_name + "_statistics.xlsx")

    logging.info(product_type_link + " finished and total number till now - " + str(items_downloaded))
    logging.info("Total items_in_multiple_categories till now - " + str(num_multiple_category_items))

    if items_downloaded > total_items_need:
        break