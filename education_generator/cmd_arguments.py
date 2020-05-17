import argparse

def getArgumentParser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('sources', metavar='SOURCE', nargs='+',
                        help='The sources for the file generation, a list of files and dirs')
    parser.add_argument('-r', dest='recursive', action='store_true',
                        help='Explore recursively the directory given as dir')
    # parser.add_argument('--correction-mode', type=int, default=0)
    parser.add_argument('--output', default='jupyter_out.ipynb')

    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Increase verbosity of output to debug')
    parser.add_argument('--write_unittest_file', dest='write_unittest_file', action='store_true', help='Write the unitest file associated with the notebook')
    parser.add_argument('--add_correction', dest='add_correction', action='store_true')
    parser.add_argument('--run', dest='run', action='store_true', )

    args = parser.parse_args()

    return args
