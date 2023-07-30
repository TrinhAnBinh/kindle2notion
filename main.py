import json
from processor import Processor, PATH
from notion import Notion

# load configuration
f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']

# construct the processor
processor = Processor(PATH)
processor.collect_highlight()
processor.process_notes()
processor.convert_book()

# construct the notion and create the page
notion = Notion(books=processor.books, secret=secret, database=database, url=url)
notion.convert_books_to_notion_inputs()
notion.prepare_header()
notion.create_pages()
# query and save the pages information into the file
pages_infor_path = 'pages.json'
notion.get_pages(pages_infor_path=pages_infor_path)