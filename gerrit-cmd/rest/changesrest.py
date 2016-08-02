import restbase as base

class Changes:
    def __init__(self):
        self.Endpoints='changes'

class ChangeEndpoints(Changes):
    @staticmethod
    def query_changes(self,**kwargs):
        return base.GerritRestAPI.get()

