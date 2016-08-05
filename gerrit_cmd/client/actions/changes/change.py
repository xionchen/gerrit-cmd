import gerrit_cmd.rest.restbase as restbase
import prettytable
import  json
endpoint_base='/changes/'

def print_table(result):
    t = prettytable.PrettyTable(result.keys())
    attrs = []
    for atr in result.keys():
        attrs.append(result.get(atr))

    t.add_row(attrs)
    print t



def query_run(config):
    rest=restbase.GerritRestAPI()
    query_list = []
    n=config.pop('n')
    querystr='?n=%d'%n
    queryargs=''

    for x in config.keys():
        if config.get(x) is not None:
            query_list.append('%s:%s'%(x,config.get(x)))

    if len(query_list)!=0:
        queryargs='&q='+'%20'.join(query_list)

    querystr=querystr+queryargs
    result=restbase.GerritRestAPI().get(endpoint_base+querystr)

    #this should be writed as a function but the situation is special.
    t = prettytable.PrettyTable(result[0].keys())

    for x in result:
        attrs = []
        if x.get('topic') == None:
            x[u'topic'] = '\'NONE\''
        if x.get('_more_changes') != None:
            x.pop('_more_changes')
        for atr in result[0].keys():
            attrs.append(x.get(atr))
        t.add_row(attrs)
    print t


def create_run(config):

    if config.get('project') is None:
        config['project'] = raw_input('please enter project:\n')
    if config.get('subject') is None:
        config['subject'] = raw_input('please enter subject:\n')
    if config.get('branch') is None:
        config['branch'] = raw_input('please enter branch:\n')
    if config.get('topic') is None:
        config['topic'] = raw_input('please enter topic:\n')
    if config.get('status') is None:
        config['status'] = raw_input('please enter status:\n')

    print 'creating'

    '''temp test code
    create_dic={
    "project" : "openstack-dev/sandbox",
    "subject" : "Let's support 100% Gerrit workflow direct in browser",
    "branch" : "master",
    "topic" : "create-change-in-browser",
    "status" : "OPEN"
  }
    '''
    sentjson= json.JSONEncoder().encode(config)
    result = restbase.GerritRestAPI().post(endpoint_base,data=sentjson)
    print_table(result)