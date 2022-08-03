from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Amsterdam Apartments List"
sheet.append(
    ['Title', 'Location', 'Price', 'Area', 'Total Rooms']
)

try:
    url = requests.get('https://www.pararius.com/apartments/amsterdam')
    url.raise_for_status()

    soup = BeautifulSoup(url.content, 'html.parser')

    lists = soup.find_all('section',
                          class_='listing-search-item')

    for list in lists:
        title = list.find('a', class_='listing-search-item__link listing-search-item__link--title').text
        location = list.find('div', class_='listing-search-item__location').get_text(strip=True)
        price = list.find('div', class_='listing-search-item__price').get_text(strip=True)
        area = list.find('li', class_='illustrated-features__item illustrated-features__item--surface-area').get_text(
            strip=True)
        total_rooms = list.find('li',
                                class_='illustrated-features__item illustrated-features__item--number-of-rooms').get_text(
            strip=True)
        print(title, location, price, area, total_rooms)

        sheet.append([title, location, price, area, total_rooms])


except Exception as e:
    print("Exception occurred due to :" + " " + str(e))

excel.save("Top Amsterdam Apartments.xlsx")
