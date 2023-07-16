import json, requests

secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

f.close()


page_id = '4a6804a3-bcfe-46d0-9a69-21ece355279b'

# Headers
headers = {
	'Authorization': f'Bearer {secret}',
	'Content-Type': 'application/json',
	'Notion-Version': '2022-06-28'
}

url = f'https://api.notion.com/v1/blocks/{page_id}/children'

data = {
    'children': [{
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{ "type": "text", "text": { "content": "binh" } }]
            }
        },
        {
            'object': 'block',
            'type': 'paragraph',
            'paragraph': {
                "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": 'binh.trinha',
                                }
                            }
                        ]
            }
        }
    ]
}
response = requests.patch(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json())
    print('Page updated successfully!')
else:
    print(f'Failed to update page. Status code: {response.status_code}')
    print(response.json())