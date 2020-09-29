'''
	Author: Husnul
'''

import ujson, sys, os, time, json, urllib3
from datetime import datetime

today = datetime.now().strftime('%Y%m%d')
start_page = int(sys.argv[1])
max_page = int(sys.argv[2])
start_date = sys.argv[3]
end_date = sys.argv[4]

dir_loc = f'{your_dir_loc}'
sub_domain = f'{your_zendesk_subdomain}'

def get_json(start_page, max_page):
    http = urllib3.PoolManager()
    uname = f'{your_username}'
    passw =  f'{your_password}'
    users = []
    print(f'dumping json...')


    for page in range(start_page,max_page+1):
        url = f'{sub_domain}/api/v2/users.json?role[]=end-user&query=updated_at>{start_date}+updated_at<{end_date}&page={page}'
        print(f'iterating page: ',page)
        
        headers = urllib3.util.make_headers(basic_auth='dodi.amar@ovo.id:OvobigData2020!!!')
        response = http.request('GET', url, headers=headers )
        data_json = response.data
        data = json.loads(data_json)
    
        users.extend(data['users'])

        try:
            if data.get('users', not []):
                with open(f'{dir_loc}/{today}.json','w') as f:
                    ujson.dump(users, f)
            else:
                print(f'end of page {page}')
                sys.exit(0)
        except Exception as e:
            print('job error...')
            print(e)
            sys.exit(1)

start_prc = time.time()
get_json(start_page, max_page)
end_prc = time.time()
est = end_prc-start_prc
print(f'=================================== DONE!')
print(f'Time elapsed: '+'{:.2f}'.format(est))
