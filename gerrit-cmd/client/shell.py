import argparse
import importlib




def run(parser):
    config = parser.__dict__
    modstr = "gerrit-cmd.client.actions.%s.%s" % config.pop("category"),config.pop("action")
    mod = importlib.import_module(modstr)
    func = getattr(mod,"run")
    return func(config)

def main():
    rootparser = argparse.ArgumentParser(description='A client for gerrit')


    subparsers = rootparser.add_subparsers(title="categories", dest="category")

    changeparsers(subparsers)

    parser = rootparser.parse_args()

    try:
        run(parser)
    except Exception as e:
        raise e
    else:
        return 0

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



if __name__=="__main__":
    main()
