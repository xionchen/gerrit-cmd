import rest.restbase as rest
import json
from requests.auth import HTTPDigestAuth
# auth = HTTPDigestAuth('XiangChen','oV1dm/Wed+KyQ2NugNwd67H1vf/gOADYPfBYfkS3UA')
'''
rest = rest.GerritRestAPI(url='http://review.openstack.org')
changes = rest.get("/changes/?")




import prettytable





t = prettytable.PrettyTable(changes[0].keys())

for x in changes:
    attrs=[]
    if x.get('topic') == None:
       x[u'topic']='\'NONE\''
    if x.get('_more_changes')!=None:
        x.pop('_more_changes')


    for atr in changes[0].keys():
        attrs.append(x.get(atr))

    t.add_row(attrs)

print t
'''
auth = HTTPDigestAuth('', '')
datadict = {
    "project": "myproject",
    "subject": "Let's support 100% Gerrit workflow direct in browser",
    "branch": "master",
    "topic": "create-change-in-browser i lvoe fc",
    "status": "DRAFT"
         }
json = json.JSONEncoder().encode(datadict)

rest = rest.GerritRestAPI(url='http://review.openstack.org', auth=auth)

result = rest.get('/changes/', json=json)

for x in result:
    print (x)