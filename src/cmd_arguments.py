import argparse

def getArgumentParser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sources', metavar='SOURCE', nargs='+',
                        help='The sources for the file generation, a list of files and dirs')
    parser.add_argument('-r', dest='recursive', action='store_true',
                        help='Explore recursively the directory given as dir')
    parser.add_argument('--correction-mode', type=int, default=0)
    parser.add_argument('--output', default='jupyter_out.ipynb')


    args = parser.parse_args()

    return args

