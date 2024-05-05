class TargetValueMapping:
    def __init__(self):
        self.Certified = 0
        self.Denied = 1
    
    def reverse_mapping(self):
        mapping = self.__dict__
        return dict(zip(mapping.values(), mapping.keys()))
