'''
	Author: Husnul
'''

import requests, ujson, os
from datetime import datetime

today = datetime.now().strftime('%Y%m%d')
dir_loc = f'{your_dir_loc}'

def get_json():
    uname = f'{your_username}'
    passw = f'{your_password}'
    groups = []

    for page in range(1,10):
        print(f'iterating page: {page}')
        url = f'{zendesk_api_url}'
        response = requests.get(url, auth=(uname,passw))
        data = response.json()
        groups.extend(data['groups'])
        if data.get('groups', not []):
            print('dumping')
            with open(f'{dir_loc}/{today}.json','w') as f:
                ujson.dump(groups, f)
        else:
            print(f'end of next page, ended with last page {page}')
            break

get_json()
