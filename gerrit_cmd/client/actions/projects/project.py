import gerrit_cmd.rest.restbase as restbase
import prettytable
import json
import urllib

endpoint_base = '/projects/'

def create_run(config):
    project_name = config.pop('name')
    project_name = urllib.quote(project_name)
    project_name = project_name.replace('/','%2F')

    data = {}
    if config.get('parent'):
        data['parent'] = config.pop('parent')
    if config.get('description'):
        data['description'] = config.pop('description')
    if config.get('branches'):
        data['branches'] = config.pop('branches')
    if config.get('owners'):
        data['owners'] = config.pop('owners')

    sentjson = json.JSONEncoder().encode(data)
    # print 'sent content: %s' % sentjson
    resutl = restbase.GerritRestAPI().put(endpoint_base+project_name, data = sentjson)
    print_table(resutl, resutl.keys())

def get_run(config):
    project_name = config.pop('name')
    project_name = urllib.quote(project_name)
    project_name = project_name.replace('/', '%2F')
    result = restbase.GerritRestAPI().get(endpoint_base + project_name)
    print_table(result,result.keys())

def list_run(config):
    substring = None
    n = None
    list_list = []
    # print config
    if config.get('substring'):
        substring = config.pop('substring')
        substring = urllib.quote(substring)
        substring = substring.replace('/','%2F')
        list_list.append('m=%s' % substring)
    if config.get('n'):
        n = config.pop('n')
        list_list.append('n=%s' % n)
    list_str = '&'.join(list_list)
    if list_list:
        list_url_str = endpoint_base + '?' + list_str + '&d'
    else:
        list_url_str = endpoint_base + '?d'
    # print list_url_str
    result = restbase.GerritRestAPI().get(list_url_str)

    result_list = transformer_list_result(result)
    print_table(result_list,['name','state','description'])

def transformer_list_result(result ):
    result_list = []
    for x in result.keys():
        project = {}
        project['name'] = urllib.unquote(x)
        for key_of_project in result[x].keys():
            project[key_of_project] = result[x][key_of_project]
        result_list.append(project)
    return result_list



def print_table(result,title):
    """

    :param result: what do you want to print
    :param title: what content do you want to print
    :return: nothing
    """
    if len(result) ==0:
        print 'got nothing'
        return
    if type(result) is dict:
        tmp_list = []
        tmp_list.append(result)
        result = tmp_list
    t = prettytable.PrettyTable(title)

    for x in result:
        attrs = []
        for atr in title:
            attr_in_row = x.get(atr)
            if attr_in_row is None:
                attr_in_row='Not Found'
            attrs.append(attr_in_row)

        t.add_row(attrs)
    print t