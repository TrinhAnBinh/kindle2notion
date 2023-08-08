import json
from processor import Processor, PATH
from notion import Notion
from checkpoint import Checkpoint

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

# construct checkpoint
check = Checkpoint('checkpoint.json')

# load checkpoint
checkpoint = check.load()
books = processor.books
# filter highlight base on the checkpoint
updated_books = []
for book in books:
    for cp in checkpoint:
        if book['book_name'] == cp['book_name']: # old book
            max_position = cp['block_offset']
            if max_position < len(book['note']): # book was added new notes
                book['note'] = book['note'][max_position:] 
                book['location'] = book['location'][max_position:] 
            else:
                book['note'] = []
                book['location'] = []
    updated_books.append(book)

# todo : should process the book in one step when create the updated_books
books_input = []
for ubook in updated_books:
    if len(ubook['note']) > 0:
        books_input.append(ubook)

# todo create the mode :update book or created book

# construct the notion and create the page
notion = Notion(books=books_input, secret=secret, database=database, url=url)
notion.convert_books_to_notion_inputs()
notion.prepare_header()
check_point = notion.create_pages()
# query and save the pages information into the file
pages_infor_path = 'pages.json'
notion.get_pages(pages_infor_path=pages_infor_path)


# update check point data
updated_page_infor = check.construct_checkpoint(check_point)
# save checkpoint to file
check.save(updated_page_infor)

# processor.collect_highlight() >> processor.process_notes()