
import re, requests, json
from time import sleep
# from notion.client import NotionClient


path = './My Clippings.txt'
with open(path, "r") as f:
	raw_hl = f.readlines()
	highlights = []
	for i in raw_hl:
		i = re.sub(r'\n', '', i)
		i = re.sub(r'\ufeff\ufeff\ufeff', '', i)
		i = re.sub(r'\ufeff', '', i)
		highlights.append(i)
	book = []
	location = []
	break_line = []
	highl = []
	new_line = []
	notes = []
	number_notes = int(len(highlights)/5)
	for i in range(number_notes):
		book.append(highlights[5*i])
		location.append(highlights[5*i+1])
		break_line.append(highlights[5*i+2])
		highl.append(highlights[5*i+3])
		new_line.append(highlights[5*i+4])
		# print(highlights[5*i].index('('))
		# print(highlights[5*i].index(')'))
		# print(highlights[5*i][11,36])
		try:
			author = highlights[5*i][highlights[5*i].index('(') + 1:highlights[5*i].index(')')]
		except:
			author = ''
		note = {
			'book_name' : highlights[5*i].strip(),
			'author' : author,
			'note' : highlights[5*i+3].strip(),
			'location' : highlights[5*i+1].strip()
		}
		notes.append(note)
	# print(notes[0])
	books_names = []
	data = []
	for n in notes:
		if n['book_name'] not in books_names:
			book_i = {
				'book_name' : n['book_name'],
				'author': n['author'],
				'note': [n['note']],
				'location' : [n['location']]
			}
			data.append(book_i)
			books_names.append(n['book_name'])
		else:
			for d in data:
				if n['book_name'] == d['book_name']:
					d['note'].append(n['note'])
					d['location'].append(n['location'])

	secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'

	# Notion Application


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
	
	for j in data:
		for k in range(len(j['note'])):
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
								"content": j['author']
								}
							},
						]
				},
				"title": {
					"title": [
					{
						"text": {
						"content": j['book_name']
						}
					},
					]
				}
				}
				,"children": [
					{
						"object": "block",
						"type": "heading_3",
						"heading_3": {
							"rich_text": [{ "type": "text", "text": { "content": j['location'][k] } }]
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
										"content": j['note'][k],
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
			sleep(1)

