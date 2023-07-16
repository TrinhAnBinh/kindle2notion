import re, requests, json
from time import sleep, time

path = './test.txt'
path = 'My Clippings.txt'
END_HIGHLIGH = '=========='
def process_clipping(path):
	with open(path, "r") as f:
		raw_hl = f.readlines()
		highlights = []
		note = []
		for i in raw_hl:
			i = re.sub(r'\n', '', i).strip()
			i = re.sub(r'\ufeff\ufeff\ufeff', '', i).strip()
			i = re.sub(r'\ufeff', '', i).strip()
			i.replace('- ', '')
			if i == END_HIGHLIGH:
				highlights.append(note)
				note = []
			else:
				if i != '':
					if '|' in i:
						location, modify_time = i.split('|')
						note.append(location.strip().replace('- ',''))
						note.append(modify_time.strip())
					else:
						note.append(i)
		return highlights[:len(highlights)]

highlights = process_clipping(path) # todo need to remove duplicate in the list

def process_notes(highlights: list) -> list:
	notes = []
	for h in highlights:
		book_name = h[0]
		# get the author name
		if '(' and ')' in book_name:
			start_point = book_name.index('(')
			end_point = book_name.index(')')
			author = book_name[ start_point + 1: end_point]
		else:
			author = ''
		init_note = h[3]
		for i in range(3, len(h)):
			init_note += '. '+h[i]
		note = {
			'book_name' : h[0],
			'author' : author,
			'location': h[1],
			'modify_time' : h[2],
			'note' : init_note
		}
		notes.append(note)
	return notes
notes = process_notes(highlights)

def convert_book(notes : list) -> list:
	'''
	input: list of notes.
	out: list of book with notes.
	'''
	books_names = []
	data = []
	for n in notes:
		if len(n['note']) > 2000:
			n['note'] = n['note'][:1995] + '...'
		if len(n['location']) > 100:
			n['location'] = n['location'][:95] + '...'
		if n['book_name'] not in books_names:
			book_item = {
				'book_name' : n['book_name'],
				'author': n['author'],
				'note': [n['note']],
				'location' : [n['location']]
			}
			data.append(book_item)
			books_names.append(n['book_name'])
		else:
			for d in data:
				if n['book_name'] == d['book_name']:
					d['note'].append(n['note'])
					d['location'].append(n['location'])
	return data

data = convert_book(notes)

secrets_key = 'secret_GvWVcVtp70axJ1JeKXNdrBOlkz0q5RJaD8lDk1Ldbz7'
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

f.close()

# Headers
headers = {
	'Authorization': f'Bearer {secret}',
	'Content-Type': 'application/json',
	'Notion-Version': '2022-06-28'
}

def create_data_input(data):
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
				,"children": children[:100] # todo need to create a function to update the page, because when creating a page, Notion only accept 100 blocks for children
			}
			data_inputs.append(data_input)
		return data_inputs

def create_pages(data_inputs):
	if data_inputs[0]:
		pages_infor = []
		for data_input in data_inputs:
			# create notion page
			with requests.Session() as ses:
				response = ses.post(url, headers=headers, json=data_input)
				page_infor = response.json()
				pages_infor.append(page_infor)
				with open('book_info.json', "a") as b:
					json.dump(pages_infor,b)
			sleep(1)

data_inputs = create_data_input(data)
create_pages(data_inputs)