from processor import Processor, PATH
import json, requests, time, datetime
from checkpoint import logger

today = datetime.datetime.now().strftime('%Y-%m-%d')

class Notion:
    def __init__(self, books, secret, database, url, updated_books):
        self.books = books
        self.secret = secret
        self.database = database
        self.url = url 
        self.root_url = 'https://api.notion.com/v1/pages/'
        self.notion_data_input = list
        self.header = dict
        self.page_id = str
        self.basic_sort = {
                            "sorts": [
                                {
                                    "property": "Last Edited",
                                    "direction": "ascending"
                                }
                            ]
                        }
        self.updated_books = updated_books
    
    def prepare_header(self) -> dict:
        if self.secret:
            self.header  =  {
                'Authorization': f'Bearer {self.secret}',
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            }
        else:
            BaseException('secret is null, set the secret first')

    def convert_books_to_notion_inputs(self, book_notes):
        '''
            Get the book notes and convert to notion data input following the formated inputs.
            Notion API: https://developers.notion.com/reference/post-page
        '''
        if book_notes:
            data_inputs = []
            # data_updates = []
            for j in book_notes:
                if len(j['note']) > 0: # filtering book have more than one note
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
                        "parent": { "database_id": self.database },
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
                        ,"children": children # todo need to create a function to update the page, because when creating a page, Notion only accept 100 blocks for children
                    }
                    data_inputs.append(data_input)
            self.notion_data_input =  data_inputs
            return data_inputs
        else:
            BaseException('Books notes have no data, rerun the pipeline')
    
    def create_page(self, book):
        with requests.Session() as ses:
            response = ses.post(self.url, headers=self.header, json=book)
            if response.status_code == 200:
                page_infor = response.json()
            else:
                raise BaseException(f'Status code - {response.status_code} !')
        self.page_id = page_infor['id']
        return page_infor['id'] # page_id
    
    def update_page_block(self, page_id: str, content: dict) -> str:
        '''
            Function to update content for given pages
        '''
        # url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        url = f'https://api.notion.com/v1/blocks/{self.page_id}/children'
        with requests.Session() as ses:
            response = ses.patch(url, headers=self.header, json=content)
            if response.status_code == 200:
                return 'Updated !'
            else:
                return f'Not yet - status code: {response.status_code}'

    def update_page_blocks(self, books):
        if books:
            checkpoint = []
            for ix, book in enumerate(books):
                if book:
                    book_name = book['properties']['title']['title'][0]['text']['content']
                    page_id = self.updated_books[ix]['page_id']
                    if len(book['children']) < 100:
                        updated_block = {
                            'children' : book['children']
                        }
                        status = self.update_page_block(page_id, updated_block)
                        book_info = {'book_name': book_name, 'page_id': page_id, 'database_id': self.database, 'block_offset': len(self.updated_books[ix]['note']), 'created_time': today, 'updated_time': today}
                        checkpoint.append(book_info)
                    else:
                        lock_input = book.copy()
                        start = 0
                        num_of_blocks = 99
                        while start < len(lock_input['children']):
                            end = start + num_of_blocks
                            if end >= len(lock_input['children']):
                                end = len(lock_input['children'])
                            updated_block = {
                                'children' : lock_input['children'][start : end]
                            }
                            status = self.update_page_block(page_id, updated_block)
                            time.sleep(1)
                            start += num_of_blocks 
                        book_info = {'book_name': book_name, 'page_id': page_id, 'database_id': self.database, 'block_offset': len(self.updated_books[ix]['note']), 'created_time': today, 'updated_time': today}
                        checkpoint.append(book_info)
                else:
                    logger.info('Book have no new notes')
            return checkpoint
        else:
            logger.info('List of books are null')

    def create_pages(self, books): # how to retrieve the pages information as checkpoint formated data
        '''
            Create multiple pages based on the data inputs
        '''
        checkpoint = []
        for ix, book in enumerate(books):
            book_name = book['properties']['title']['title'][0]['text']['content']
            if len(book['children']) >= 100:
                lock_input = book.copy()
                ini_block = book['children'][:100]
                book.update({
                    'children': ini_block
                })
                page_id = self.create_page(book)
                start = 100
                num_of_blocks = 99
                while start < len(lock_input['children']):
                    end = start + num_of_blocks
                    if end >= len(lock_input['children']):
                        end = len(lock_input['children'])
                    updated_block = {
                        'children' : lock_input['children'][start : end]
                    }
                    status = self.update_page_block(page_id,updated_block)
                    time.sleep(1)
                    start += num_of_blocks
                book_info = {'book_name': book_name, 'page_id': page_id, 'database_id': self.database, 'block_offset': len(self.books[ix]['note']), 'created_time': today, 'updated_time': today}
                checkpoint.append(book_info)
            else:
                page_id  = self.create_page(book)
                book_info = {'book_name': book_name, 'page_id': page_id, 'database_id': self.database, 'block_offset': len(self.books[ix]['note']), 'created_time': today, 'updated_time': today}
                checkpoint.append(book_info)
        return checkpoint
    
    def delete_page(self, page_id):
        option = {
            'archived': False,
        }
        url = self.root_url + page_id
        with requests.Session() as ses:
            response = requests.patch(url, headers=self.header, json=option)
            if response.status_code == 200:
                status = 'Deleted'
            else:
                raise BaseException(f'Faile with status code - {response.status_code}')
    
    def get_pages(self, pages_infor_path) -> str:
        '''
            Function to update content for given pages
        '''
        url = f'https://api.notion.com/v1/databases/{self.database}/query'
        with requests.Session() as ses:
            response = ses.post(url, headers=self.header, json=self.basic_sort)
            if response.status_code == 200:
                with open(pages_infor_path, 'w', encoding='utf-8') as f:
                    # f.write(json.dumps(response.json(), ensure_ascii=False).encode('utf-8'))
                    json.dump(response.json(), f, ensure_ascii=False)
            else:
                return f'Not yet - status code: {response.status_code}'
    