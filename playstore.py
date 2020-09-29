'''
	how to run: python3.6 playstore_crawler.py [job_id]
	this script will crawl daily review metadata such as username, title review, content, etc.
	how it works: 
		- crawl data to max record
		- save it to .json file
'''


from google_play_scraper import Sort, reviews
import json
import sys

job_id = sys.argv[1]

#getreview
def getResult():
    result = reviews(
        f{'apps_id'},
        lang='id',
        country='id',
        count=99999999,
        sort=Sort.NEWEST
    )
    return result

#save result to json
def saveJson():
    result = getResult()
    with open(f'{your_json_dir_loc}'),'w') as f:
        f.write(json.dumps(result, indent=4, sort_keys=True, default=str))

if __name__ == '__main__':
    getResult()
    saveJson()
