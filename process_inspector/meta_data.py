class MetaData:
    def __init__(self):
        self.case_attr = {}
        self.obj_attr = {}
        self.info = {}
        
    def add_case_attr(self, case, attr, value):
        if case not in self.case_attr:
            self.case_attr[case] = {}
        self.case_attr[case][attr] = value
        
        
    def add_obj_attr(self, obj, attr,value):
        if obj not in self.obj_attr:
            self.obj_attr[obj] = {}
        self.obj_attr[obj][attr] = value
        
    def get_case_attr(self, case, attr):
        value = None
        try:
           value = self.case_attr[case][attr]
        except KeyError as e:
            pass
        return value
    
    def get_obj_attr(self, obj, attr):
        value = None
        try:
            value = self.obj_attr[obj][attr]
        except KeyError as e:
            pass
        return value