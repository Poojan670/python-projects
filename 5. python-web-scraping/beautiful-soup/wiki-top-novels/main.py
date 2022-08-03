from bs4 import BeautifulSoup
import requests
import pandas as pd

try:
    url = requests.get('https://en.wikipedia.org/wiki/List_of_best-selling_light_novels')
    url.raise_for_status()

    soup = BeautifulSoup(url.text, 'html.parser')

    table = soup.find('table')

    titles = []
    for i in table.find_all('th'):
        title = i.text.strip()
        titles.append(title)

    df = pd.DataFrame(columns=titles)

    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')

        row_data = [td.i.a.text if td.i is not None else td.get_text(strip=True) for td in data]
        length = len(df)
        df.loc[length] = row_data

    print(df)

    df.to_excel("TOP SELLING LIGHT NOVELS OF ALL TIME.xlsx")
    print("TOP LN table scrapped and excel sheets exported successfully!")

except Exception as e:
    print("Exception occurred due to :" + " " + str(e))
