Gerrit-cmd
==========

This project is a cmd tool for gerrit.
It's being developing now and can't wort yet.

Installation
============

On linux:
---------

1. install pip(This can be different acording to what your linux is)
2. $ git clone https://github.com/xionchen/gerrit-cmd.git
3. $ cd gerrit-cmd
4. $ pip install .
5. edit your configuration file reference to "Configuration"

On windowns:
------------

1. install pip
2. Download the project form https://github.com/xionchen/gerrit-cmd
3. In cmd:
  a. enter the gerrit-cmd path
  b. run pip "install ."
4. edit your configuration file under your %HOMEPATH% (usually it's C:/user/username)
   reference to "Configuration"

**note**:cmd in windows do not support utf-8,so there may be some messy code, if you
use Chinese.Pipeline the result to a file is a way to deal with this problem.
    example:gerrit_cmd change query -p problem_name -s status\
    -n number--print-message > log.file

Usage examples
==============

query the message in changes:

    gerrit_cmd change query -p problem_name -s status -n number --print-message


Configuration
=============
All the configuration are configured in ~/.grtrc

Configuration options
---------------------

| **url**：The url of you gerrit server,this must be configured
| **username**:The user name of your gerrit,this is not necessary if you don't want to be authorized by gerrit server.
| **password**:The HTTP password of your gerrit,this is not necessary if you don't want to be authorized by gerrit server.

Example
-------
| There is an example configure file: /grtrc_example
| All the options should be configured in "grt" section

::

    [grt]
    url=review.openstack.org
    username=username
    password=password

Extend the code
===============

How to extend
-------------

There are 3 layers of this project: shell, actions, restbase.
shell decide how to deal with argument and pass the arguments to one module of actions.
In actions module, the specific of actions are defined with function actionname_run() and
will use restbase module.

To extend the code:

- add a xxxxparsers reference to changeparsers in client.shell.shell.py
- add actions in action module

Rest Api
--------

There are rest api which you can reference to:
https://review.openstack.org/Documentation/rest-api.html

Copyright and License
=====================

License
-------

Licensed under The MIT License.  Please refer to the `LICENSE` file for full
license details.

Copyright
---------

Some codes are based on the project https://github.com/sonyxperiadev/pygerrit

Some codes reference this project  https://github.com/pyKun/scalpels
