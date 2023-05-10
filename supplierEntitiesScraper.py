from requests.models import Response
import pandas as pd
from bs4 import BeautifulSoup
import requests
from csv import writer

print('initiating scraper')

df = pd.read_csv('iranwatch_suppliers.csv')
df = pd.DataFrame(df)
df = df.dropna()


url_list = []
for i in df['Link']:
  root_url = 'https://www.iranwatch.org'
  url_list.append(root_url + str(i))


entity_name = []
alias = []
entity_address = []
phone_number = []
company_website = []
country = []
exporting_country = []
weapon_program = []
date_of_activity = []
suspect_entities_suppliers = []
content = []
created_date = []
last_updated_date = []
profile_picture = []

for item in url_list:
    raw_html = requests.get(item)
    soup = BeautifulSoup(raw_html.text, 'html.parser')

    entity_name.append(soup.find('h1', id='page-title').get_text().replace('\n','').strip())
    try: 
       alias.append(soup.find('section', class_='field field-name-field-old-aka field-type-text-long field-label-above view-mode-full').find('div', class_='field-items').get_text())
    except:
       alias.append('') 
    try:
       phone_number.append(soup.find('section', class_= 'field field-name-field-old-e-mail field-type-text-long field-label-above view-mode-full').get_text())
    except: 
       phone_number.append('')
    try:
        company_website.append(soup.find('section', class_="field field-name-field-old-url-field field-type-text-long field-label-above view-mode-full").get_text())
    except:
       company_website.append('')
    try: 
       country_section = soup.find('section', class_="field field-name-field-country field-type-taxonomy-term-reference field-label-above view-mode-full")
       country_ul = country_section.find('ul', class_='field-items')
       country_li = country_ul.find_all('li', class_='field-item')
       country_item = [country_li.text.strip() for country_li in country_ul]
       country.append(tuple(country_item))
    except:
       country.append('')
    try:
       exporting_country.append(soup.find('section', class_='field field-name-field-old-exporting-country field-type-text field-label-above view-mode-full').find('div', class_='field-items').get_text())
    except:
       exporting_country.append('')
    try:
       weapon_program.append(soup.find('section', class_="field field-name-field-weapon-program field-type-taxonomy-term-reference field-label-above view-mode-full").find('ul', class_='field-items').get_text())
    except:
       weapon_program.append('')
    try:
       date_of_activity.append(soup.find('section', 'field field-name-field-date-of-iran-related-activ field-type-text field-label-above view-mode-full').find('div', class_='field-items').get_text())
    except: 
       date_of_activity.append('')  
    try:
       entity_address.append(soup.find('section', class_='field field-name-field-old-address field-type-text-long field-label-above view-mode-full').find('div', class_='field-items').get_text())
    except:
       entity_address.append('')
    try:
       section = soup.find('section', class_='field field-name-field-mentioned-suspect-entities field-type-entityreference field-label-above view-mode-full')
       divs = section.find_all('div', class_='field-item')
       items = [div.text.strip() for div in divs]
       suspect_entities_suppliers.append(tuple(items))
       
    except:
      suspect_entities_suppliers.append([''])
          

    try:
       content.append(soup.find('div', 'field field-name-body field-type-text-with-summary field-label-hidden view-mode-full').get_text())
    except:
       content.append('')
    try:
       created_date.append(soup.find('section', class_='field field-name-field-date-entered field-type-datetime field-label-inline clearfix view-mode-full').find('div', class_='field-items').get_text())
    except:
       created_date.append('')
    try:
       last_updated_date.append(soup.find('section', class_='field field-name-field-date-last-modified field-type-datetime field-label-inline clearfix view-mode-full').find('div', class_='field-items').get_text())
    except:
       last_updated_date.append('')
    try: 
      profile_picture.append(soup.find('div', class_="field field-name-field-image field-type-image field-label-hidden view-mode-full").find('figure', class_='clearfix field-item even' ).find('a').get("href"))
    except: 
      profile_picture.append('')



print('Data scraped. Writing to JSON')

df = pd.DataFrame({
   "Entity": entity_name, 
   "Alias": alias,
   "Address": entity_address,
   "phone_number": phone_number,
   "company_website": company_website,
   "Country": country,
   "Exporting Country": exporting_country,
   "Weapon Program": weapon_program,
   "Date of Activity": date_of_activity,
   "Suspected Links": suspect_entities_suppliers,
   "Information": content,
   "Created": created_date,
   "Last_updated": last_updated_date,
   "profile_picture" : profile_picture
}
)


dictionary = df.to_json(orient="records", indent=4)
print(dictionary)

with open('iranianSuppliers.json','w') as outfile:
   outfile.write(dictionary)



print('----Task completed-----')