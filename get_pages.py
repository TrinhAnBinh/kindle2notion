import requests
import json

# secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

f.close()

filter_query = {
    "sorts": [
        {
            "property": "Last Edited",
            "direction": "ascending"
        }
    ]
}


def get_pages(database: str, content) -> str:
    '''
    function to update content for given pages
    '''
    # Headers
    headers = {
        'Authorization': f'Bearer {secret}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    url = f'https://api.notion.com/v1/databases/{database}/query'
    with requests.Session() as ses:
        response = ses.post(url, headers=headers, json=content)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Not yet - status code: {response.status_code}'

pages = get_pages(database, filter_query)
page_info = json.dumps(pages)

with open('pages_info.json', 'w') as f:
    f.write(page_info)

