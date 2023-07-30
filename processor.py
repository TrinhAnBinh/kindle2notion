import re

PATH = 'test.txt'

class Processor:
    '''
        The Processor is abstract receive the path of kindle clipping and return structured/formated data
    '''
    def __init__(self, path):
        self.path = path
        self.END_HIGHLIGH = '=========='
        self.highlights = []
        self.notes = []
        self.books = []
        self.MAX_CHARACTER_IN_BLOCK = 2000
        self.MAX_CHARACTER_IN_HEADING = 100
    
    def collect_highlight(self) -> list:
        '''
            Construct the list to collect highlights, each combo highligh is structured as list
            A combo of highligh in the clipping file of kindle
            --------------begin---------------
            ﻿Big Data Analytics  -> book name
            - Your Highlight on page 35-35 | Added on Sunday, May 29, 2022 10:40:48 AM -> location

            this section we propose a novel data science and analytics application system design methodology -> content
            ========== -> end of highlight
            --------------end---------------
            highlight = [highligh1, highligh2]
            highligh1 = [book_name, location, content, end of highlight]
        '''
        with open(self.path, "r") as f:
            lines = f.readlines()
            highlights = []
            note = []
            for line in lines:
                line = re.sub(r'\n', '', line).strip()
                line = re.sub(r'\ufeff\ufeff\ufeff', '', line).strip()
                line = re.sub(r'\ufeff', '', line).strip()
                line.replace('- ', '')
                if line == self.END_HIGHLIGH:
                    highlights.append(note)
                    note = []
                else:
                    if line != '':
                        if '|' in line:
                            location, modify_time = line.split('|')
                            note.append(location.strip().replace('- ',''))
                            note.append(modify_time.strip())
                        else:
                            note.append(line)
            self.highlights = highlights
            # return highlights[:-2]  # remove the empty string 
        
    def process_notes(self) -> list:
        '''
            Process the raw highlight in clipping and reconstruct the formated note.
        '''
        notes = []
        if self.highlights:
            for h in self.highlights:
                book_name = h[0]
                # get the author name
                if '(' and ')' in book_name:
                    start_point = book_name.index('(')
                    end_point = book_name.index(')')
                    author = book_name[ start_point + 1: end_point]
                else:
                    author = ''
                note_content = h[3]
                for i in range(4, len(h)):
                    note_content += '. '+ h[i]
                note = {
                    'book_name' : h[0],
                    'author' : author,
                    'location': h[1],
                    'modify_time' : h[2],
                    'note' : note_content
                }
                notes.append(note)
            self.notes = notes
        else:
            raise BaseException('Highlights is empty, Run the collect_highlight method!')

    def convert_book(self) -> list:
        '''
            Get the note and convert to book note. Book note is multiple note for each book
        '''
        books_names = []
        data = []
        for n in self.notes:
            if len(n['note']) > self.MAX_CHARACTER_IN_BLOCK: 
                n['note'] = n['note'][:1995] + '...' 
            if len(n['location']) > self.MAX_CHARACTER_IN_HEADING:
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
        self.books = data

processor = Processor(PATH)
processor.collect_highlight()
processor.process_notes()
processor.convert_book()

# # test processor
# print(processor.notes[5])
# # test convert book
print(processor.books[3]['note'])
