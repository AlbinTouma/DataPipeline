from requests.models import Response
import pandas as pd
from bs4 import BeautifulSoup
import requests
from csv import writer


print('initiating scraper')

df = pd.read_csv('iranwatch_sanctionedcompanies.csv')
df = pd.DataFrame(df)
df = df.dropna()


url_list = []
for i in df['Link']:
  root_url = 'https://www.iranwatch.org'
  url_list.append(root_url + str(i))

entity_name = []
linked_entity = []
suspect_entities_suppliers = []


#Get the names of entity

for item in url_list[0:14]:
    raw_html = requests.get(item)
    soup = BeautifulSoup(raw_html.text, 'html.parser')
    
    entity_name.append(soup.find('h1', id='page-title').get_text().replace('\n','').strip())


#Get names of each of the linked entities
for item in url_list[0:14]:
    raw_html = requests.get(item)
    soup = BeautifulSoup(raw_html.text, 'html.parser')
    
    try:
       section = soup.find('section', class_='field field-name-field-mentioned-suspect-entities field-type-entityreference field-label-above view-mode-full')
       divs = section.find_all('div', class_='field-item')
       items = [div.text.strip() for div in divs]
       suspect_entities_suppliers.append(tuple(items))
       
    except:
      suspect_entities_suppliers.append([''])


url  = []
#Get url of each of the linked entities
for item in url_list[0:14]:
    raw_html = requests.get(item)
    soup = BeautifulSoup(raw_html.text, 'html.parser')
    
    try:
       section = soup.find('section', class_='field field-name-field-mentioned-suspect-entities field-type-entityreference field-label-above view-mode-full')
       divs = section.find('div', class_='field-item')
       items = divs.find('a')
       href = items.get('href')
       url.append(href)
       
    except:
      url.append([''])



print(len(entity_name))
print(len(suspect_entities_suppliers))


df = pd.DataFrame(
   {
   "Entity": entity_name,
    "Link": suspect_entities_suppliers,
    "url": url
   }
)


dictionary = df.to_json(orient="records", indent=4)

print(dictionary)

#with open('linksTest.json','w') as outfile:
#   outfile.write(dictionary)
