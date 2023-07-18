import json
import requests

# secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']
f.close()

page_id = '4a6804a3-bcfe-46d0-9a69-21ece355279b'

data = {
        'children': [{
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "binh"}}]
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


def update_children(page_id: str, content: dict) -> str:
    '''
    function to update content for given pages
    '''
    # Headers
    headers = {
        'Authorization': f'Bearer {secret}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    with requests.Session() as ses:
        response = ses.patch(url, headers=headers, json=content)
        if response.status_code == 200:
            return 'Updated'
        else:
            return f'Not yet - status code: {response.status_code}'
