import gerrit_cmd.rest.restbase as restbase
import prettytable
import  json
endpoint_base='/changes/'

def print_table(result):

    t = prettytable.PrettyTable(result.keys())
    attrs = []
    for atr in result[0].keys():
        attrs.append(result.get(atr))

    t.add_row(attrs)
    t.add_column()



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
        for atr in result.keys():
            attrs.append(x.get(atr))
        t.add_row(attrs)
    print t


def create_run(config):

    if not config.has_key():
        config['project'] = raw_input('please enter project:\n')
        
    create_dic['subject'] = raw_input('please enter subject:\n')
    create_dic['branch'] = raw_input('please enter branch:\n')
    create_dic['topic'] = raw_input('please enter topic:\n')
    create_dic['status'] = raw_input('please enter status:\n')


    '''temp test code
    create_dic={
    "project" : "openstack-dev/sandbox",
    "subject" : "Let's support 100% Gerrit workflow direct in browser",
    "branch" : "master",
    "topic" : "create-change-in-browser",
    "status" : "OPEN"
  }
    '''
    sentjson= json.JSONEncoder().encode(create_dic)
    result = restbase.GerritRestAPI().post(endpoint_base,data=sentjson)
    print_table(result)