import json
from processor import Processor, PATH
from notion import Notion
from checkpoint import Checkpoint
import logging
# Configure the logger
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level to DEBUG (you can adjust this)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Create a logger instance
logger = logging.getLogger('main')

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
def filter_books(books):
    if books:
        if checkpoint:
            new_books = []
            updated_books = []
            mode_books = []
            for book in books:
                for cp in checkpoint:
                    if book['book_name'] == cp['book_name']: # old book
                        book.update({
                            "page_id" : cp['page_id'],
                            'mode': 'update'
                        })
                        max_position = cp['block_offset']
                        if max_position < len(book['note']): # book was added new notes
                            book['note'] = book['note'][max_position:] 
                            book['location'] = book['location'][max_position:] 
                        else:
                            book['note'] = []
                            book['location'] = []
                    else:
                        book.update({
                            'mode' : 'create'
                        })
                mode_books.append(book)
            for book in mode_books:
                if len(book['note']) > 0:
                    if book['mode'] == 'create':
                        new_books.append(book)
                    elif book['mode'] == 'update':
                        updated_books.append(book)
            if not new_books:
                logger.info('No new book for this part')
            if not updated_books:
                logger.info('No new notes to updated book')    
            return new_books, updated_books
        else:
            return books, []

new_books, updated_books = filter_books(books)
if not new_books and not updated_books:
    logger.info('No new books and block for books')
else:
    # construct the notion and create the page
    notion = Notion(books=new_books, secret=secret, database=database, url=url, updated_books=updated_books)
    notion.prepare_header()
    check_point = []
    if new_books:
        _new  = notion.convert_books_to_notion_inputs(new_books)
        check_points_new = notion.create_pages(books=_new)
        for check_point_new in check_points_new:
            check_point.append(check_point_new)
    if updated_books:
        _updated = notion.convert_books_to_notion_inputs(updated_books)
        check_points_updated = notion.update_page_blocks(books=_updated)
        for check_point_updated in check_points_updated:
            check_point.append(check_point_updated)
    
    # query and save the pages information into the file
    pages_infor_path = 'pages.json'
    notion.get_pages(pages_infor_path=pages_infor_path)

    # update check point data
    updated_page_infor = check.construct_checkpoint(check_point)
    # save checkpoint to file
    check.save(updated_page_infor)

    # processor.collect_highlight() >> processor.process_notes()