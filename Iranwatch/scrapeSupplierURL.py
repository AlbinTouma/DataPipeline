import pandas as pd
from bs4 import BeautifulSoup
import requests
from csv import writer

#Scrape Iranian entities names
def scraper(url: str) -> None:
  max_pages = 37
  current_page = 0

  with open('iranwatch_suppliers.csv', 'w', encoding='utf8', newline='') as f:
      thewriter = writer(f)
      header = ['Source', 'Link']
      thewriter.writerow(header)

      while current_page <= max_pages:
        current_url = f'{url}?page={current_page}'
 
        raw_html = requests.get(current_url)
        soup = BeautifulSoup(raw_html.text, 'html.parser')

        list = soup.find_all('span', class_='field-content')
        for i in list:
                    i.find('span', class_='field-content') 
                    list = i.get_text().replace('\n', '') #we replace spaces with blanks
                    try:
                      link = i.find('a')['href']
                    except:
                      link = None
                    info = [list, link]
                    thewriter.writerow(info)  #this tells csv writer to write lists and links on each row.
                    
                   
                
            
        current_page += 1

scraper('https://www.iranwatch.org/suppliers')