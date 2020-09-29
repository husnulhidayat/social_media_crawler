'''
        Author: Husnul
'''

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys
import json

job_id = sys.argv[1]

def getData(start_page, end_page):
    list_result=[]
    for page in range(start_page, end_page+1):
        print(f'iterating page {page}')
        url = f'{appstore_lxml_url}'
        page_n = requests.get(url)
        source = bs(page_n.text, 'lxml')
        results = source.find_all('entry')
        
        for result in results:
            idd = result.find('id').text
            name = result.find('name').text
            title = result.find('title').text
            content = result.find('content').text
            date = result.find('updated').text
            rating = result.find('im:rating').text
            version = result.find('im:version').text

            list_result.append({
                'id': idd,
                'name': name,
                'title': title,
                'content': content,
                'date': date,
                'rating': rating,
                'version': version
            })
            
    print(f'done iterating, start dumping...')
    gluster_d= f'{your_dir_loc}'
    with open(gluster_d,'a+') as f:
        f.write(json.dumps(list_result, indent=2))
    print(f'dumping to json finished.')
                
getData(1,10)
