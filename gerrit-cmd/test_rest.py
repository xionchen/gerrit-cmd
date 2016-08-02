import rest.rest as rest
from requests.auth import HTTPDigestAuth
auth = HTTPDigestAuth('XiangChen','oV1dm/Wed+KyQ2NugNwd67H1vf/gOADYPfBYfkS3UA')

rest = rest.GerritRestAPI(url='http://review.openstack.org', auth=auth)
changes = rest.get("/changes/?q=owner:self%20status:open")
print changes

import prettytable



print changes[0]
print changes[0].keys()

t = prettytable.PrettyTable(changes[0].keys())

for x in changes:
    attrs=[]
    for atr in x.keys():
        attrs.append(x.get(atr))

    t.add_row(attrs)

print t