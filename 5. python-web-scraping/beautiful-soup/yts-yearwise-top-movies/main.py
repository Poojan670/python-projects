# System imports
import sys
from random import randint

# Excel Export Module
import openpyxl

# Requests URL Module
import requests

# Web Scrapper Helper
from bs4 import BeautifulSoup


def excel_config(year):
    """
    Excel Config for openpyxl excel config
    :param year:
    :return excel & sheet:
    """
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = f"Top Movies for the year {year}"
    sheet.append(
        ['SN', 'title', 'year', 'rating', 'genre', 'language']
    )

    return excel, sheet


def web_scrapping():
    """
    Web Scrapping for yts along with paginated scrapping
    :return:
    """
    excel, sheet = excel_config(input_year)

    SN = 1
    flag = True

    try:
        for page in range(1, 1000):
            if flag:
                if page == 1:
                    url = requests.get(f"https://yts.mx/browse-movies/0/all/all/0/rating/{input_year}/all")
                else:
                    url = requests.get(f"https://yts.mx/browse-movies/0/all/all/0/rating/{input_year}/all?page={page}")
                url.raise_for_status()

                soup = BeautifulSoup(url.text, 'html.parser')

                movies = soup.find('section').find_all('div', class_='browse-movie-wrap')
                if not movies:
                    break
                for movie in movies:

                    language = "[Eng]"

                    title = movie.find('div', class_='browse-movie-bottom').a.text
                    if title[0] == "[":
                        language = title[0:4]
                        title = title[5:]

                    year = movie.find('div', class_='browse-movie-year').text
                    if year != input_year:
                        flag = False
                        break

                    try:
                        rating = movie.find('h4', class_='rating').text
                    except AttributeError:
                        rating = None

                    genres_data = movie.find('figcaption', class_='hidden-xs hidden-sm').get_text(strip=True)
                    a = genres_data.rfind('10')
                    b = genres_data.rfind('View')
                    genre = genres_data[a + 2:b]

                    SN += 1

                    print(SN, title, year, rating, genre, language)
                    sheet.append([SN, title, year, rating, genre, language])
        try:
            # Save the sheet as Excel file
            excel.save(f'yts top movies of {input_year}.xlsx')
            print("Script Successfully Completed")
        except FileExistsError:
            # For multiple testings
            num = randint(1, 1000)
            excel.save(f'yts top movies of {input_year} {num}.xlsx')
            print("Script Successfully Completed")

    except Exception as e:
        print("Exception occurred due to :" + " " + str(e))
        print("Script Failed, Please try again!")
        # Exit the script if exception
        sys.exit()


if __name__ == '__main__':
    """
    Main Py Script
    """
    input_year = str(input("Enter the year you want to scrape !! "))

    web_scrapping()  # scrapping function call
