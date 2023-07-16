
import re, requests, json
from time import sleep, time

path = './My Clippings.txt'
def process_clipping(path):
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
		# process list of notes
		for i in range(number_notes):
			book.append(highlights[5*i])
			location.append(highlights[5*i+1])
			break_line.append(highlights[5*i+2])
			highl.append(highlights[5*i+3])
			new_line.append(highlights[5*i+4])
			book_name = highlights[5*i]
			# get the author name
			if '(' and ')' in book_name:
				start_point = highlights[5*i].index('(')
				end_point = highlights[5*i].index(')')
				author = highlights[5*i][ start_point + 1: end_point]
			else:
				author = ''
			note = {
				'book_name' : book_name.strip(),
				'author' : author,
				'note' : highlights[5*i+3].strip(),
				'location' : highlights[5*i+1].strip()
			}
			notes.append(note)
		# convert list of notes to list of books
		books_names = []
		data = []
		for n in notes:
			if len(n['note']) > 2000:
				n['note'] = n['note'][:2000]
			if len(n['location']) > 100:
				print(n)
				n['location'] = n['location'][:100]
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
		return data

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

# load configuration

f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

f.close()

# secret = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
# database = '23899900a2ab41b0b399d4f388a91325'
# url = 'https://api.notion.com/v1/pages'




# Headers
headers = {
	'Authorization': f'Bearer {secret}',
	'Content-Type': 'application/json',
	'Notion-Version': '2022-02-22'
}

def create_data_input():
	data = process_clipping(path=path)
	if data:
		data_inputs = []
		for j in data:
			children = []
			for k in range(len(j['note'])):
				header = {
							"object": "block",
							"type": "heading_3",
							"heading_3": {
								"rich_text": [{ "type": "text", "text": { "content": j['location'][k] } }]
							}
						}
				children.append(header)
				para = {
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
				children.append(para)
				
			# Data input
			data_input = {
				"parent": { "database_id": database },
				'icon': {
					'type': "emoji",
						'emoji': "🥬"
				},
				'cover': {
					'type': "external",
					'external': {
						'url': "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
					}
				},
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
				,"children": children
			}
			data_inputs.append(data_input)
		return data_inputs

def create_pages(data_inputs):
	if data_inputs[0]:
		pages_infor = []
		for data_input in data_inputs:
			# create notion page
			ses = requests.Session()
			response = ses.post(url, headers=headers, json=data_input)
			if response.status_code != 200:
				print('err begin')
				print(data_input)
				print('err end')
				break
			page_infor = response.json()
			pages_infor.append(page_infor)
		with open('book_info.json', "a") as b:
			json.dump(pages_infor,b)
		sleep(1)

data_inputs = create_data_input()
create_pages(data_inputs)

# with open('book_info.json','r') as book:
# 	b = json.load(book)
# 	print(b)


