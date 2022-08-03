from bs4 import BeautifulSoup
import requests
import pandas as pd

url = requests.get('https://www.nfl.com/standings/league/2021/REG')
url.raise_for_status()

soup = BeautifulSoup(url.text, 'html.parser')

league_name = soup.find('section',
                        class_='d3-l-grid--outer d3-l-section-row nfl-o-standings').find(
    'div', class_='d3-o-standings--table-header'
).find_all('div')[1].text


table = soup.find('table', {'summary': 'Standings - Detailed View'})

titles = []
for i in table.find_all('th'):
    title = i.text.strip()
    titles.append(title)

df = pd.DataFrame(columns=titles)

for row in table.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    print(row_data)
    length = len(df)
    df.loc[length] = row_data

print(df)

df.to_excel('NFL LEAGUE TABLE.xlsx')
print("NFL League table scrapped and excel sheets exported successfully!")

