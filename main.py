import json
from processor import Processor, PATH
from notion import Notion
from checkpoint import Checkpoint
from checkpoint import logger
from unidecode import unidecode

def load_config():
    # load configuration
    f = open('config.json')
    conf = json.load(f)
    secret = conf['api_token']
    database = conf['database']
    url = conf['root_url']
    return secret, database, url

def exe_pipe(instance, pipe, seperator = '>>'):
    run_pipes = pipe.split(seperator)
    for f in run_pipes:
        f = f.strip()
        func = getattr(instance, f)
        if callable(func):
                func()
        else:
            logger.error(f"Error: '{f}' is not a callable function.")

def filter_books(books, checkpoint):
    '''
        Filter highlight base on the checkpoint
    '''
    if books:
        if checkpoint:
            new_books = []
            updated_books = []
            mode_books = []
            old_books = [cp['book_name'].lower().strip() for cp in checkpoint]
            for book in books:
                if book['book_name'].lower().strip() in old_books:
                    # list of old books need to updated notes
                    for cp in checkpoint:
                        if book['book_name'].lower().strip() == cp['book_name'].lower().strip(): # old book
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
                    # New books need to create pages
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

# load configuration
secret, database, url = load_config()
# construct the processor
processor = Processor(PATH)
exe_pipe(processor,'collect_highlight >> process_notes >> convert_book')
# construct checkpoint
check = Checkpoint('checkpoint.json')
# load checkpoint
checkpoint = check.load()
# load books
books = processor.books
# filter books
new_books, updated_books = filter_books(books, checkpoint)

if not new_books and not updated_books:
    logger.info('No new books and blocks for books')
else:
    # construct the notion
    notion = Notion(books=new_books, secret=secret, database=database, url=url)
    check_point = []
    if new_books:
        # create new_books
        _new  = notion.convert_books_to_notion_inputs(new_books)
        check_points_new = notion.create_pages(books=_new)
        for check_point_new in check_points_new:
            check_point.append(check_point_new)
    if updated_books:
        # update old books
        _updated = notion.convert_books_to_notion_inputs(updated_books)
        check_points_updated = notion.update_page_blocks(books=_updated, updated_books=updated_books)
        for check_point_updated in check_points_updated:
            check_point.append(check_point_updated)

    # query and save the pages information into the file
    pages_infor_path = 'pages.json'
    notion.get_pages(pages_infor_path=pages_infor_path)
    # update check point data
    updated_page_infor = check.construct_checkpoint(check_point)
    # save checkpoint to file
    check.save(updated_page_infor)
