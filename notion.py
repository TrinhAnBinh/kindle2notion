from processor import Processor, PATH
import json



class Notion:
    def __init__(self, books, secret, database, url):
        self.books = books
        self.secret = secret
        self.database = database
        self.url = url 
        self.notion_data_input = []

    def convert_books_to_notion_inputs(self):
        '''
            Get the book notes and convert to notion data input following the formated inputs.
            Notion API: https://developers.notion.com/reference/post-page
        '''
        if self.books:
            data_inputs = []
            # data_updates = []
            for j in self.books:
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
        else:
            BaseException('Books notes have no data, rerun the pipeline')

f = open('config.json')
conf = json.load(f)
secret = conf['api_token']
database = conf['database']
url = conf['root_url']



processor = Processor(PATH)
processor.collect_highlight()
processor.process_notes()
processor.convert_book()

# test processor
print(processor.notes[5])
# test convert book
print(processor.books[0])

notion = Notion(books=processor.books, secret=secret, database=database, url=url)
notion.convert_books_to_notion_inputs()

print(notion.notion_data_input)