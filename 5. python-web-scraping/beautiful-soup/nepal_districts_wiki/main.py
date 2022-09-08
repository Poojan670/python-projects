from random import randint

from bs4 import BeautifulSoup
import requests
import openpyxl


def excel_config():
    """
    Excel Config for openpyxl excel config
    :param year:
    :return excel & sheet:
    """
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"Districts of Nepal"
    sheet.append(
        ['English']
    )

    return excel, sheet


def excel_configs():
    """
    Excel Config for openpyxl excel config
    :param year:
    :return excel & sheet:
    """
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"Districts of Nepal"
    sheet.append(
        ['Nepali']
    )

    return excel, sheet


url = requests.get('https://en.wikipedia.org/wiki/List_of_districts_of_Nepal')
url.raise_for_status()

soup = BeautifulSoup(url.text, 'html.parser')

excel, sheet = excel_config()
excel1, sheet1 = excel_config()

main_div = soup.find('div', class_='mw-body-content mw-content-ltr')
tables = main_div.find_all('table', class_='wikitable sortable')
for table in tables[1:]:
    tbody = table.find_all('tbody')
    for body in tbody:
        tr = body.find_all('tr')
        for data in tr:
            td = data.find_all('td')
            for i in td:
                try:
                    english_name = i.a.text.strip()
                    sheet.append([english_name])
                    print(english_name)
                except AttributeError:
                    nepal_name = i.text.strip()
                    print(nepal_name)
                    sheet1.append([nepal_name])
                    break

try:
    # Save the sheet as Excel file
    excel.save("districts of nepal.xlsx")
    excel1.save("districts of nepal1.xlsx")
    print("Script Successfully Completed")
except FileExistsError:
    # For multiple testings
    num = randint(1, 1000)
    excel.save(f'districts of nepal {num}.xlsx')
    print("Script Successfully Completed")
