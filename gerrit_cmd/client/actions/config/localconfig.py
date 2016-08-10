import ConfigParser
import platform
import os


def makeconfig():
    """
    config the config file
    :return:
    """
    url = raw_input('please enter the url of your gerrit server\n>> ')
    username = raw_input('please enter the username of your gerrit\n>> ')
    password = raw_input('please enter https password of your gerrit\n>> ')
    cf = ConfigParser.ConfigParser()
    cf.add_section('grt')

    cf.set('grt', 'url', url)
    cf.set('grt', 'username', username)
    cf.set('grt', 'password', password)

    home = ''
    if platform.system()=='Windows':
        home = os.environ['HOMEPATH']
    else:
        home = os.environ['HOME']

    config_path = home + '/.grtrc'
    cf.write(open(config_path, 'w'))
