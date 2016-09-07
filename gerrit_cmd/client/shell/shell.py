import argparse
import importlib

# map category to it's category parent
mapper = {'change': 'changes',
          'change_edit': 'changes',
          'project': 'project'

          }


def map(category):
    result = mapper.get(category)
    if result is None:
        print ('%s not find ' % category)
        raise Exception
    else:
        return result


def run(parser):
    config = parser.__dict__
    category = config.pop("category")
    modstr = "gerrit_cmd.client.actions.%s.%s" % (map(category), category)
    # print modstr
    mod = importlib.import_module(modstr)
    func = getattr(mod, "%s_run" % config.pop('action'))

    return func(config)


def main():
    rootparser = argparse.ArgumentParser(description='A client for gerrit')
    subparsers = rootparser.add_subparsers(title="categories", dest="category")

# Add paraser arguments in respective parsers, just like a pipeline. one should just modify the function they care
# and make sure action in gerrit_cmd.actions are available
    accessparaser(subparsers)
    accountsparaser(subparsers)
    changeparsers(subparsers)
    projectparaser(subparsers)

    parser = rootparser.parse_args()
    run(parser)


def changeparsers(subparsers):
    # ###change categories
    changeparsers = subparsers.add_parser("change")
    change_subparsers = changeparsers.add_subparsers(title="actions", dest="action")

    # ##change query
    change_query_parsers = change_subparsers.add_parser("query")

    change_query_parsers.add_argument("-s", "--status",
                                      choices=['open', 'reviewed', 'closed', 'merged', 'abandoned'],
                                      dest='status', help='status of the change')

    change_query_parsers.add_argument('-O', '--owner', dest='owner',
                                      help='Changes originally submitted by \'USER\'.  '
                                           'The special case of owner:self will find '
                                           'changes owned by the caller.')

    change_query_parsers.add_argument('-I', '--ID', dest='ID',
                                      help='A legacy numerical \'ID\' such as 15183, '
                                           'or a newer style Change-Id that was scraped '
                                           'out of the commit message')

    change_query_parsers.add_argument('-p', '--project', dest='projects',
                                      help='query changes about this project.(or projects starting with this argument)')

    change_query_parsers.add_argument('-n', dest='n', default=25,
                                      help='How many changes do you want.Default 25')

    change_query_parsers.add_argument('--print-message', dest='print-message', action='store_true',
                                      help='print message')




    '''
    change_query_parsers.add_argument('-o', dest='o',
                                      help='Additional fields can be obtained by adding o parameters, each option '
                                           'requires more database lookups and slows down the query response time '
                                           'to the client so they are generally disabled by default.')
    '''

    # ##change create
    change_create_parsers = change_subparsers.add_parser("create")
    change_create_parsers.add_argument('-p', '--project', dest='project')
    change_create_parsers.add_argument('-s', '--subject', dest='subject')
    change_create_parsers.add_argument('-b', '--branch', dest='branch')
    change_create_parsers.add_argument('-t', '--topic', dest='topic')
    change_create_parsers.add_argument('--status', dest='status')

    # ##change detail
    change_id_help = 'Identifier that uniquely identifies one change.\n' \
                     'This can be:\n' \
                     '''an ID of the change in the format "'<project>~<branch>~<Change-Id>'",''' \
                     ' where for the branch the refs/heads/ prefix can be omitted' \
                     ' ("myProject~master~I8473b95934b5732ac55d26311a706c9c2bde9940")\n' \
                     'a Change-Id if it uniquely identifies one change ' \
                     '("I8473b95934b5732ac55d26311a706c9c2bde9940")\n' \
                     'a legacy numeric change ID ("4247")\n'

    change_create_parsers = change_subparsers.add_parser("detail")
    change_create_parsers.add_argument('-i', '--id', dest='id', help=change_id_help)

    # ##change message
    change_message_parsers = change_subparsers.add_parser("message")
    change_message_parsers.add_argument('-n', dest='n', default=25, help='How many changes do you want.Default 25')


def projectparaser(subparsers):

    projectparaser = subparsers.add_parser("project")
    project_sub_parsers = projectparaser.add_subparsers(title="actions", dest="action")

    project_create_parsers = project_sub_parsers.add_parser("create")

    project_create_parsers.add_argument('--name', dest='name', required = True)
    project_create_parsers.add_argument('--description', dest='description')
    project_create_parsers.add_argument('--submit_type', dest='submit_type')
    project_create_parsers.add_argument('--owners', dest='owners', nargs='+')


def accessparaser(subparsers):
    # do access related paraser here
    pass

def accountsparaser(subparsers):
    # do account related paraser here
    pass

def configparaser(subparsers):
    # ###change categories
    configparaser = subparsers.add_parser("config")
    config_subparsers = changeparsers.add_subparsers(title="actions", dest="action")


if __name__ == "__main__":
    main()
