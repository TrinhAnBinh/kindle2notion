import json, requests
import re

secret = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'

page_id = '76bbffca-d83e-471e-8ab0-1f2eac70211a'
root_url = 'https://api.notion.com/v1/pages/'

database = '23899900a2ab41b0b399d4f388a91325'
url = root_url + page_id

url_2 = 'https://api.notion.com/v1/pages/42277092-b33f-4603-8816-232691c7b795'

if url == url_2:
    print('ok')

# Headers
headers = {
    'Authorization': f'Bearer {secret}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-02-22'
}

data_input = {
    'archived': False,
}

response = requests.patch(url, headers=headers, json=data_input)
print(response.json())
# sleep(1)