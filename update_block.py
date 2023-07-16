# curl 'https://api.notion.com/v1/blocks/b55c9c91-384d-452b-81db-d1ef79372b75/children?page_size=100' \
#   -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
#   -H "Notion-Version: 2022-02-22"


import json, requests

secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

f.close()


page_id = '623b1cc4-bb84-49c8-bf7a-2c88c8c92d35'


# Headers
headers = {
	'Authorization': f'Bearer {secret}',
	'Content-Type': 'application/json',
	'Notion-Version': '2021-05-13'
}

url = f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100'

response = requests.patch(url, headers=headers)

if response.status_code == 200:
    # print('Page updated successfully!')
    print(response.json())
else:
    print(f'Failed to update page. Status code: {response.status_code}')
    print(response.json())