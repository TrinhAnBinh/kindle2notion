import requests

secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'

# Notion Application
import json, requests


# file = open('SECRET.json') # Opens the file

# data = json.load(file) # loads the data then stores in variable called data

# # Secret here:
# secret = data['id']

# # Database information here:
# database = data['database_tasks']

# file.close() # close file

# https://www.notion.so/9cdd1313b73e4fffa4d1f4ea364b7262?v=8672984de76246f78301b5a3122fc6ca


secret = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
database = '23899900a2ab41b0b399d4f388a91325'
url = 'https://api.notion.com/v1/pages'

# Headers
headers = {
    'Authorization': f'Bearer {secret}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-02-22'
}

# Data input
data_input = {
    "parent": { "database_id": database },
    "properties": {
        'Author': {
            'id': 'KDEZ',
            'type': 'rich_text',
            'rich_text': [
                {
                    "text": {
                    "content": "Trinh An Binh"
                    }
                },
            ]
    },
      "title": {
        "title": [
          {
            "text": {
              "content": "Ngon lanh post duoc data"
            }
          },
        ]
      }
    }
    ,"children": [
		{
			"object": "block",
			"type": "heading_2",
			"heading_2": {
				"rich_text": [{ "type": "text", "text": { "content": "Lacinato kale" } }]
			}
		},
		{
			"object": "block",
			"type": "paragraph",
			"paragraph": {
				"rich_text": [
					{
						"type": "text",
						"text": {
							"content": "phan nay la highlight",
						}
					}
				]
			}
		}
	]
  }
# check request 
response = requests.post(url, headers=headers, json=data_input)
print(response.json())

