import json
import sys

import openpyxl
import requests
from bs4 import BeautifulSoup


def excel_config():
    """
    Excel Config for openpyxl excel config
    :return excel & sheet:
    """
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"List of municipalities english"
    sheet.append(
        ['province', 'district', 'local_level_name', 'type']
    )

    return excel, sheet


province = []
district = []
palika = []


def province_name_helper(province_name):
    if len(province_name) == 1:
        return f"Province No {province_name}"
    else:
        return province_name


def province_helper(province_name) -> None:
    province_name = province_name_helper(province_name)

    if len(province) == 0:
        province.append({
            "model": "core.Province",
            "pk": len(province) + 1,
            "fields": {
                "name": province_name,
                "is_default": False,
                "active": True,
                "created_date_ad": "2022-08-19 10:52:29.068719+05:45",
                "created_date_bs": "2079-08-21",
                "created_by": 1
            }
        })

    flag = False
    for data in province:
        if province_name == data["fields"]["name"]:
            flag = True

    if not flag:
        province.append({
            "model": "core.Province",
            "pk": len(province) + 1,
            "fields": {
                "name": province_name,
                "is_default": False,
                "active": True,
                "created_date_ad": "2022-08-19 10:52:29.068719+05:45",
                "created_date_bs": "2079-08-21",
                "created_by": 1
            }
        })


def province_fk_calc(province_name):
    for data in province:
        if province_name_helper(province_name) == data["fields"]["name"]:
            return data["pk"]


def district_helper(district_name: str, province_name: str) -> None:
    province_fk = province_fk_calc(province_name)
    if len(district) == 0:
        district.append({
            "model": "core.District",
            "pk": len(district) + 1,
            "fields": {
                "name": district_name.title(),
                "is_default": False,
                "active": True,
                "province": province_fk,
                "created_date_ad": "2022-08-19 10:52:29.068719+05:45",
                "created_date_bs": "2079-08-21",
                "created_by": 1
            }
        })

    flag = False
    for data in district:
        if district_name.title() == data["fields"]["name"]:
            flag = True
    if not flag:
        district.append({
            "model": "core.District",
            "pk": len(district) + 1,
            "fields": {
                "name": district_name.title(),
                "is_default": False,
                "active": True,
                "province": province_fk,
                "created_date_ad": "2022-08-19 10:52:29.068719+05:45",
                "created_date_bs": "2079-08-21",
                "created_by": 1
            }
        })


def palika_name_validator(palika_name) -> str:
    if "Rural Municipality" in palika_name:
        palika_name = palika_name.replace("Rural Municipality", "Gaupalika")
    elif "Sub-Metropolitian City" in palika_name:
        palika_name = palika_name.replace("Sub-Metropolitian City", "Upa-Mahanagarpalika")
    elif "Metropolitian City" in palika_name:
        palika_name = palika_name.replace("Metropolitian City", "Mahanagarpalika")
    else:
        palika_name = palika_name.replace("Municipality", "Nagarpalika")
    return palika_name


def district_fk_calc(district_name):
    for data in district:
        if district_name.title() == data["fields"]["name"]:
            return data["pk"]


def palika_helper(palika_name: str, district_name: str) -> None:
    district_fk = district_fk_calc(district_name)
    # district_fk = [data["pk"] for data in district if data["fields"]["name"] == district_name.title()]
    palika_name = palika_name_validator(palika_name)
    model = "core.Palika"
    palika.append({
        "model": model,
        "pk": len(palika) + 1,
        "fields": {
            "name": palika_name,
            "is_default": False,
            "active": True,
            "province": district_fk,
            "created_date_ad": "2022-08-19 10:52:29.068719+05:45",
            "created_date_bs": "2079-08-21",
            "created_by": 1
        }
    })


def web_scraping():
    """
    Web Scraping for nepalese municipalities
    """
    # excel, sheet = excel_config()

    url = requests.get('https://www.nepalgov.com/list-of-municipalities-and-rural-municipalities-english/')
    url.raise_for_status()

    try:
        soup = BeautifulSoup(url.text, 'html.parser')

        tbody = soup.find("tbody", class_="row-hover")

        count = 0
        for body in tbody:
            if count % 2 != 0:
                province_name = body.find("td", class_="column-1").text
                district_name = body.find("td", class_="column-2").text
                level_name = body.find("td", class_="column-3").text

                # type = body.find("td", class_="column-4").text
                province_helper(province_name)

                district_helper(district_name, province_name)
                palika_helper(level_name, district_name)
                # sheet.append([province, district, level_name, type])
            count = count + 1

            # excel.save("municipalities.xlsx")
    except Exception as e:
        print("Exception occurred due to :" + " " + str(e))
        print("Script Failed, Please try again!")
        # Exit the script if exception
        sys.exit()


if __name__ == '__main__':
    """
    Main Py Script
    """

    web_scraping()

    with open("province.json", "w") as f:
        json.dump(province, f)
    #
    with open("district.json", "w") as f:
        json.dump(district, f)
    #
    with open("palika.json", "w") as f:
        json.dump(palika, f)
