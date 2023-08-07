''' The object save and load, init checkpoint '''
import os
import logging
import json

# Configure the logger
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level to DEBUG (you can adjust this)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# Create a logger instance
logger = logging.getLogger('checkpoint')

class Checkpoint:
    '''
        Construct the checkpoint object to load, save pages information checkpoint.
        An example checkpoint data
        data = [
                {'book_name': '1', 'page_id': '3', 'database_id': '4', 'block_offset': '123121', 'created_time': '6', 'updated_time': '7'},
                {'book_name': '1', 'page_id': '31', 'database_id': '4', 'block_offset': '11111', 'created_time': '6', 'updated_time': '7'},
                {'book_name': '1', 'page_id': '311', 'database_id': '4', 'block_offset': '52', 'created_time': '6', 'updated_time': '7'}
            ]
    '''
    def __init__(self, path):
        self.path = path
        self.abs_path = os.path.abspath(path)
        self.keys = ['book_name','page_id','database_id','block_offset','created_time','updated_time']

    def validate_path(self) -> bool:
        if isinstance(self.path, str) and self.path and self.path.endswith('.json'):
            return True
        else:
            logger.error('File path is not valid')
            return False

    def validate_info(self, pages_info) -> bool:
        '''
            Validate the info is not null and list datatype
            Validate each item has no null value and key in list of declared keys.
        '''
        if isinstance(pages_info, list) and pages_info:
            status = True
            for item in pages_info:
                for k, v in item.items():
                    if v and k in self.keys: # check value is not null and item column is list of keys
                        status = True and status
                    else:
                        logger.error('Item is not valid')
                        status = False and status
            return status
        else:
            logger.error('Pages information is null or wrong format')

    def __init_checkpoint__(self):
        if self.validate_path():
            if os.path.exists(self.path):
                self.delete()
            with open(self.path, 'w') as f:
                logger.info(f'Init the checkpoint in {self.abs_path}')
                f.write('')

    def delete(self):
        if self.validate_path():
            try:
                os.remove(self.path)
                logger.info(f'Delete the checkpoint in {self.abs_path}')
            except FileNotFoundError as e:
                logger.error(e)
                raise e
    
    def save(self, pages_info): 
        # todo, do you think we should replace the sefl.info = local data 
        if self.validate_path():
            if self.validate_info(pages_info):
                if os.path.exists(self.path):
                    with open(self.path, 'w', encoding='utf-8') as f:
                        logger.info(f'Save data in path {self.abs_path}')
                        # f.write(json.dumps(pages_info, ensure_ascii=False).encode('utf-8'))
                        json.dump(pages_info, f, ensure_ascii=False)
                else:
                    self.__init_checkpoint__()
                    with open(self.path, 'w', encoding='utf-8') as f:
                        logger.info(f'Init and save data in path {self.abs_path}')
                        # f.write(json.dumps(pages_info, ensure_ascii=False).encode('utf-8'))
                        json.dump(pages_info, f, ensure_ascii=False)
            else:
                logger.error('Pages information is not valid')
        else:
            logger.error(f'Given file path name is not valid - {self.path}')
    
    def load(self) -> list:
        if self.validate_path():
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    try:
                        info = json.load(f)
                        logger.info(f'Load pages information - in path: {self.abs_path}')
                        return info
                    except Exception as e:
                        logger.error(f'Can not parse json data - {e}')
            else:
                logger.error(f'File path is not valid - {self.abs_path}')
        else:
            logger.error(f'Given file path name is not valid - {self.path}')
    
    def construct_checkpoint(self, pages_info):
        '''
            Create new updated pages information base on new information and old information
            Update page information - max block
        '''
        if self.validate_info(pages_info):
            try:
                old_pages = self.load()
                added_page = []
                for nv in pages_info:
                    for ix , ov in enumerate(old_pages):
                        if ov['page_id'] == nv['page_id']:   
                            ov['block_offset'] =  nv['block_offset'] # todo verify the logic, replace or accumulate the value?
                            break
                        else:
                            if ix == len(old_pages) - 1: # check is last item
                                added_page.append(nv)
                                break
                            else:
                                next
                updated_info = old_pages + added_page
                return updated_info
            except:
                return pages_info
        else:
            logger.error('Pages information is not valid')