import gerrit_cmd.rest.restbase as restbase
import prettytable
import json

endpoint_base = '/changes/'


def print_messages(result):
    resultlist = []
    # ensure result is a list
    if type(result) is dict:
        resultlist.append(result)
    else:
        resultlist = result
    messages=map(lambda x:trans_changes_to_messages(x), resultlist)

    result=[]
    for x in messages:
        for a in x:
            result.append(a)

    print_table(result)


def trans_changes_to_messages(change):

    messages = change['messages']
    id = change['id']
    change_id = change['change_id']

    for x in messages:
        x['id'] = id
        x['change_id'] = change_id

    return messages


def print_table(result):

    t = prettytable.PrettyTable(result[0].keys())

    for x in result:
        attrs = []
        for atr in result[0].keys():
            attrs.append(x.get(atr))
        if len(attrs) != 6:
            continue
        t.add_row(attrs)
    print t


def query_run(config):

    query_list = []
    n = config.pop('n')
    querystr = '?n=%s' % n
    pm = config.pop('print-message')
    optionstr = ''
    if pm is True:
        optionstr = '&o=%s' % 'MESSAGES'

    queryargs = ''

    for x in config.keys():
        if config.get(x) is not None:
            query_list.append('%s:%s' % (x, config.get(x)))

    if len(query_list) != 0:
        queryargs = '&q='+'%20'.join(query_list)

    querystr = querystr + queryargs+optionstr

    result = restbase.GerritRestAPI().get(endpoint_base+querystr)

    if pm is True:
        print_messages(result)
        return
    # this should be writed as a function but the situation is special.
    t = prettytable.PrettyTable(result[0].keys())

    for x in result:
        attrs = []
        if x.get('topic') is None:
            x[u'topic'] = '\'NONE\''
        if x.get('_more_changes') is not None:
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

    print '\ncreating>>'

    '''temp test code
    create_dic={
    "project" : "openstack-dev/sandbox",
    "subject" : "Let's support 100% Gerrit workflow direct in browser",
    "branch" : "master",
    "topic" : "create-change-in-browser",
    "status" : "OPEN"
  }
    '''
    sentjson = json.JSONEncoder().encode(config)
    result = restbase.GerritRestAPI().post(endpoint_base, data=sentjson)
    resultlist=[]
    resultlist.append(result)
    print_table(resultlist)


def detail_run(config):
    if config.get('id') is None:
        config['project'] = raw_input('No id,please enter change id:\n')

    detailstr = config.pop('id')+'/detail'
    result = restbase.GerritRestAPI().get(endpoint_base+detailstr)
    import pdb
    pdb.set_trace()
    print_table(result)


