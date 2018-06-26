import bs4 as bs
from urllib.request import Request, urlopen
import parse, json
import pandas as pd
import tqdm, time, os
import logging
import requests

exp_name = 'Macys_' + time.time().__str__()
logging.basicConfig(filename=exp_name + ".log", level=logging.INFO)

output_path = "./" + exp_name + "_data"
os.makedirs(output_path, exist_ok=False)


url = "https://www.macys.com/"

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

data = requests.get(url, headers=headers)
sauce=data.text
soup = bs.BeautifulSoup(sauce, "lxml")
woman_product_type_list=[]
woman_product_type_list2=[]
for item in soup.find_all('script', {'type': "application/json","data-mcom-header-menu-desktop":"context.header.menu"}):

    json_objects = json.loads(item.text)

    try:
        for x in range(0,60):
            woman_product_type_list.append(json_objects[0]["children"][0]["group"][0]["children"][0]["group"][x]["url"])
    except IndexError as e:
        break

for elem in woman_product_type_list:
    if elem[0] is "/":
        woman_product_type_list2.append("http://www.macys.com"+elem)

        
# Hard coded filtering for woman products
# view_all_list = set(t[0] for t in filter(lambda x: x[1].lower() == "view all", woman_product_type_list2))
# woman_product_type_set = set([k[0] for k in woman_product_type_list2]) - view_all_list
woman_product_type_set=set(woman_product_type_list2)


print(woman_product_type_set)
# Variable initializations
total_items_need, items_downloaded, num_multiple_category_items = 1000000, 0, 0
massive_json = {}
color, title, description, attributes, url_list = [], [], [], [], []

for product_type_link in tqdm.tqdm(woman_product_type_set):
    soup_product_type_page = bs.BeautifulSoup(requests.get(product_type_link, headers=headers).text, "lxml")

    for item in soup_product_type_page.find_all("a", {'class':"productDescLink"}):
        product_link = item.get("href")
        product_link="https://macys.com"+product_link
        print (product_link)
        try:
            final_object, id, first_download_of_item = parse.main(product_link, output_path, massive_json)
            if not first_download_of_item:
                num_multiple_category_items += 1
                print("Item_clash_for", item)
                continue

        except Exception as e:
            print("Parse failed for ", item, e)
            continue

        massive_json[id] = final_object

        color.append(final_object["annotation"]["color"])
        title.append(final_object["annotation"]["title"])
        description.append(final_object["annotation"]["description"])
        attributes.append(final_object["annotation"]["attributes"])
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
        data_frame["attributes"] = attributes
        data_frame["url_list"] = url_list

        data_frame.to_excel(exp_name + "_macysstats.xlsx")

        logging.info(product_type_link + " finished and total number till now - " + str(items_downloaded))
        logging.info("Total items_in_multiple_categories till now - " + str(num_multiple_category_items))

    if items_downloaded > total_items_need:
        break