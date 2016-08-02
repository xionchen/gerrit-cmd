import rest.rest as rest
from requests.auth import HTTPDigestAuth
auth = HTTPDigestAuth('XiangChen','oV1dm/Wed+KyQ2NugNwd67H1vf/gOADYPfBYfkS3UA')

rest = rest.GerritRestAPI(url='http://review.openstack.org', auth=auth)
changes = rest.get("/changes/?q=n:10")


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