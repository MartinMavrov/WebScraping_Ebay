# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 20:33:24 2021

@author: marti
"""

from bs4 import BeautifulSoup
import requests
import csv

#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import csv



response = requests.get( 'https://www.ebay.com/sch/shu590218nona/m.html?_nkw=&_armrs=1&_png=1')
soup = BeautifulSoup(response.text, 'lxml')


#print(soup)

    
    

def get_page(url):
         #print('hello')
     response = requests.get(url)
    
     if not response.ok:
             print('Server responded:', response.status_code)
     else:
        soup = BeautifulSoup(response.text, 'lxml')
     return soup
    



def get_detail_data(soup):   
    
    try: 
        title_data = soup.find('title').text
        len1 = len(title_data)
        title = title_data[:len1-8]
        #print(title)
    except:
        title = ''
        
    try:
        p = soup.find('span', id = 'prcIsum').text
        currency, price = p.split(' ')
        #print(price)
    except:
        currency = ''
        price = ''
        
    try:
        brand = soup.findAll('span', itemprop='name')[4].text
    except:
        brand = ''
        
    try:
        vendor = soup.find('span', class_='mbg-nw').text
        #print(vendor)
    except:
        vendor = ''
        
   
    try:
        description = soup.find('span', id="vi-cond-addl-info").text
        #print(description.split('.')[0])
    except:
        description = ''
    try:
        condition = soup.find('div', id = "vi-itm-cond").text
        #print(condition)
    except:
        condition = ''
        
    data = {'COGS': price,
            'Title': title,
            'Description': description,
            'Condition': condition,
            'Vendor': vendor,
            'Brand': brand
            }
        
    return data
        




def get_index_data(soup):
    try:
        links = soup.findAll('a', class_='vip')
    except:
        links = []
        
    urls = [item.get('href') for item in links]
    
    return urls



def main():
       #print('hello')
       url = 'https://www.ebay.com/sch/shu590218nona/m.html?_nkw=&_armrs=1&_png=1'
       
       
       #get_index_data(get_page(url))
    
       products = get_index_data(get_page(url))
       
       
    
       for link in products:
        data = get_detail_data(get_page(link))

        write_csv(data,link)
        
        


def write_csv(data,url):
    with open('TOutput.csv', 'a') as csvfile:
        
        writer = csv.writer(csvfile)
        
        row = [data['COGS'], data['Title'], data['Description'], data['Condition'], data['Images'], data['Vendor'],
              data['Brand'], url]
        
        writer.writerow(row)



if __name__=='__main__':
    main()









