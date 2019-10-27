import yaml
from datetime import datetime
import os

class Util:

    def read_config(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        config_folder_path = os.path.join(file_path,"../")
        with open(os.path.join(config_folder_path,"config/config.yml"), 'r') as ymlfile:
            self.config = yaml.safe_load(ymlfile)
        return self.config

    """Unique identifier for each task request received by the API"""
    def create_task_id(self):
        task_id = str(datetime.now().time())
        remove_chars = ".:"
        for char in remove_chars:
            task_id = task_id.replace(char,"")
        return task_id

    def get_path(self,config_key):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        data_folder_path = os.path.join(dir_path,"../")
        path = os.path.join(data_folder_path,self.config[config_key])
        if not os.path.exists(path):
            os.makedirs(path)
        return path