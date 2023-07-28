import re

class Processor:
    def __init__(self, path):
        self.path = path
        self.END_HIGHLIGH = '=========='
        self.highlights = []
        self.notes = []
    
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
            self.highlights = highlights[:-2]
            # return highlights[:-2]  # remove the empty string 
        
    def process_notes(self) -> list:
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
                note = {
                    'book_name' : h[0],
                    'author' : author,
                    'location': h[1],
                    'modify_time' : h[2],
                    'note' : h[3]
                }
                notes.append(note)
            self.notes = notes
        else:
            raise BaseException('Highlights is empty, Run the collect_highlight method!')



processor = Processor(path='My Clippings.txt')
processor.collect_highlight()
processor.process_notes()
# test processor
print(processor.notes[5])
