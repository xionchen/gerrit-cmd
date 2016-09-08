set -x
gerrit_cmd project get
gerrit_cmd project list -n 5
gerrit_cmd project list --substring nova -n 10
gerrit_cmd project get --name openstack/nova
gerrit_cmd project create
gerrit_cmd project create --name test/test
