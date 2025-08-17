import pandas as pd

    
class MetaData:
    def __init__(self):
        self.case_data = []
        self.obj_data = []
        self.info = {}
        
    def add_case_record(self, record):
        self.case_data.append(record)
        
    def add_obj_record(self, record):
        self.obj_data.append(record)
        
    def get_case_data(self):
        return pd.DataFrame(self.case_data)
    
    def get_obj_data(self):
        return pd.DataFrame(self.obj_data)
        