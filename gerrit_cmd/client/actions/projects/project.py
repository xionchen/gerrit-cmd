import gerrit_cmd.rest.restbase as restbase
import prettytable
import json

endpoint_base = '/projects/'

def create_run(config):
    project_name = config.pop('name')
    resutl = restbase.GerritRestAPI().put(endpoint_base+project_name)
    print resutl