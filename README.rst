gerrit-cmd
==========

This project is a cmd tool for gerrit.
It's being developing now and can't wort yet.

Configuration
=============
All the configuration are configured in ~/.grtrc

Configuration options
---------------------
url：The url of you gerrit server,this must be configured

username:The user name of your gerrit,this is not necesssary if you don't
want to be authorized by gerrit server.

password:The HTTP password of your gerrit,this is not necessary if you don't
want to be authorized by gerrit server.

example
-------

    [grt]
    url=review.openstack.org
    username=username
    password=password


Copyright and License
====================

License
-------

Copyright 2011 Sony Ericsson Mobile Communications. All rights reserved.

Copyright 2012 Sony Mobile Communications. All rights reserved.

Licensed under The MIT License.  Please refer to the `LICENSE`_ file for full
license details.

Copyright
---------

Some codes are based on the project https://github.com/sonyxperiadev/pygerrit

Some codes are referenced