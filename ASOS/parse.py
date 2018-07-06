import bs4 as bs
from urllib.request import Request,urlopen
import json, os
import subprocess
import requests
import time
import logging

product_link = "http://us.asos.com/river-island/river-island-beach-blouse-with-tie-front-in-cream/prd/9867632?CTAref=Recently+Viewed&clr=cream"
headers={
		"User-Agent": "Mozilla/5.0"
	}
req = requests.get(product_link, headers=headers)
sauce = req.text
soup = bs.BeautifulSoup(sauce, "lxml")

final_object={}

def is_number(x):
    try:
        float(x)
        return True
    except (ValueError):
        return False

# # Description
# description = ""
# for item in soup.find_all("div", {"class":"brand-description"}):
#     for elem in item.find_all("span"):
#         description += elem.text
# print(description)

# Price
# price = []
# price_string = []
# whole_text = ""
# section1 = ""
# section2 = ""
# section3 = ""
# original = ""
# sale = ""
# for item in soup.find_all("script", {"type":"text/javascript"}):
#     whole_text += item.text
# section1 = whole_text.split("price")[-1]
# section2 = section1.split("rrp")[0]
# section2 = section2.replace('"', " ")
# section3 = section2.split("{")[1]
# price_string = section3.split(",")[:-1]
# for x in range(0,2):
#     price_string[x] = price_string[x].split(":")[1]
# if price_string[1]=="0.0":
#     original = price_string[0]
#     sale = "N/A"
# else:
#     original = price_string[1]  
#     sale = price_string[0]
# price.append("Original: $" + original.strip())
# price.append("Sale: $" + sale.strip())
# print(price)


# # Color
# color = ""
# whole = ""
# section1 = ""
# section2 = ""

# for item in soup.find_all("script", {"type":"text/javascript"}):
#     whole += item.text
# section1 = whole.split("colour")[1]
# section2 = section1.split(":")[1]
# color = section2.split(",")[0]
# color = color.replace('"', "'", 2)
# color = color.split("'")[1]
# print(color)


# # Attributes
# product_name = ""
# attributes0 = ""
# attributes1 = []
# x = 0
# for item in soup.find_all("div", {"class":"product-description"}):
#     for elem in item.find_all("strong"):
#         product_name += elem.text + " by "
    
#     attributes0 = product_name[:-4]
    
#     for elem in item.find_all("li"):
#         attributes1.append(elem.text)
# print(attributes0)
# print(attributes1)


# # Title and Brand
# title = ""
# brand = ""
# variable = 0
# for elem in soup.find_all("span", {"itemprop":"name"}):
#     if variable == 1:
#         title+=elem.text
           
#     else:
#         brand+=elem.text
#         variable = 1
# title = title[:-4]

# print(title)
# print(brand)


# # Composition and Composition String
# percentage = []
# composition = []
# material_string = ""
# material_list = []
# composition_string = []
# test = ""
# content = []
# percent = []
# try:
#     for item in soup.find_all("div", {"class":"about-me"}, "span"):
#         material_string += item.text
#         try:
#             material_list = material_string.split(", ")
#         except Exception:
#             material_list.append(material)
        
#     test = material_list[0].split("ABOUT ME")[1]
#     test = test.split(":")[0] + ":"
#     test = test.strip()

#     counter = 0
#     for elem in test:
#         if elem ==":":
#             counter +=1

#     for char in test:
#         if char.isupper() == True:
#             test = test[:test.find(char)] + "?" + test[test.find(char):]
    
#     if test[0] == '?':
#         test = test[1:]
#     content = test.split("?")

#     if counter > 0:
#         composition.append(content[-1])
#         content = content[:-1]

#     content_list = []
#     for elem in content:
#         content_list.append(elem.strip())
#     content = content_list

#     material_list[0] = material_list[0].strip()
#     material_list[-1] = material_list[-1].strip()
    
#     try:
#         material_list[-1] = material_list[-1].split(".")[0]
#         material_list = material_list.split(content[-1])[1]
#     except Exception:
#         pass
#     try:
#         material_list[0] = material_list[0].split(composition[0])[1]
#     except Exception:
#         pass
#     for elem in material_list:
#         temp = elem.split("% ")[1] 
#         composition_string.append(temp.strip())
#         temp1= elem.split("% ")[0] + " "
#         try:
#             temp1 = temp1.split(content[-1])[1]
#         except Exception:
#             pass
#         try:
#             temp_mat = temp1.split(":")[0] + ":"
#             temp1 = temp1.split(": ")[1]
#         except Exception:
#             temp_mat = ""

#         percentage.append(temp_mat)
#         percentage.append(temp1.strip())
#         percent.append(temp1.strip())
#     y = 0
#     for x in range(0, len(percentage)):  
#         if percentage[x] == "":
#             pass
#         elif is_number(percentage[x]) == True:
#             composition.append(["Material: " + composition_string[y], "Percentage: " + percent[y]])
#             y+=1
#         else:
#             composition.append(percentage[x])  

# except Exception:
#     composition = "N/A"
#     composition_string = "N/A"
# print(content)
# print(composition)
# print(composition_string)

# # Categories
# categories = []
# category_string = ""
# whole_string = ""
# for item in soup.find_all("script", {"type":"text/javascript"}):
#     whole_string += item.text
# whole_string = whole_string.split("breadcrumb: '/")[1]
# category_string = whole_string.split("',")[0]
# categories = category_string.split("/")
# print(categories)
