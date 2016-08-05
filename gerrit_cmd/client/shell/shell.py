import argparse
import importlib

#map category to it's category parent
mapper = {'change'       :    'changes',
          'change_edit'  :    'changes'
         }

def map(category):
    result = mapper.get(category)
    if result is None:
         print '%s not find ' %category
         raise Exception
    else:
        return result

def run(parser):
    config = parser.__dict__
    category=config.pop("category")
    modstr = "gerrit_cmd.client.actions.%s.%s" % (map(category),category)
    #print modstr
    mod = importlib.import_module(modstr)
    func = getattr(mod,"%s_run" % config.pop('action'))

    return func(config)

def main():
    rootparser = argparse.ArgumentParser(description='A client for gerrit')
    subparsers = rootparser.add_subparsers(title="categories", dest="category")

# Add paraser arguments in respective parsers, just like a pipeline. one should just modify the function they care
# and make sure action in gerrit_cmd.actions are available
    accessparaser(subparsers)
    accountsparaser(subparsers)
    changeparsers(subparsers)

    parser = rootparser.parse_args()
    run(parser)
'''     try:
        run(parser)
    except Exception as e:
        print e
        raise e

    else:
        return 0
'''
def changeparsers(subparsers):
    ###change categories
    changeparsers = subparsers.add_parser("change")
    change_subparsers = changeparsers.add_subparsers(title="actions", dest="action")

    ##change query
    change_query_parsers = change_subparsers.add_parser("query")

    change_query_parsers.add_argument("-s", "--status",
                                      choices=['open', 'reviewed', 'closed', 'merged', 'abandoned'],
                                      dest='status', help='status of the change')

    change_query_parsers.add_argument('-o', '--owner', dest='owner',
                                      help='Changes originally submitted by \'USER\'.  '
                                           'The special case of owner:self will find '
                                           'changes owned by the caller.')

    change_query_parsers.add_argument('-I', '--ID', dest='ID',
                                      help='A legacy numerical \'ID\' such as 15183, '
                                           'or a newer style Change-Id that was scraped '
                                           'out of the commit message')

    change_query_parsers.add_argument('-n', dest='n',default=25,
                                      help='How many changes do you want.Default 25')

    ##change create
    change_create_parsers = change_subparsers.add_parser("create")
    change_create_parsers.add_argument('-p','--project',dest='project')
    change_create_parsers.add_argument('-s','--subject',dest='subject')
    change_create_parsers.add_argument('-b','--branch',dest='branch')
    change_create_parsers.add_argument('-t','--topic',dest='topic')
    change_create_parsers.add_argument('-s','--status',dest='status')


def accessparaser(subparsers):
    #do access related paraser here
    pass

def accountsparaser(subparsers):
    # do account related paraser here
    pass




if __name__=="__main__":
    main()
