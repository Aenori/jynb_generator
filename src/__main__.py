import os

import cmd_arguments
from file_to_jupyter_notebook import FileToJupyterNotebook

def main():
    args = cmd_arguments.getArgumentParser()

    if args.debug:
        

    file_list = getFileList(args)

    file_to_jupyter_notebook = FileToJupyterNotebook(
        write_unittest_file = args.write_unittest_file, 
        add_correction = args.add_correction
    )
    file_to_jupyter_notebook.convertFileListToNotebook(file_list, args.output)

def extractFilesFromSourceDir(source_dir, recursive):
    raise NotImplementedError()  

def getFileList(args):
    file_list = []
    for it_source in args.sources:
        if os.path.isfile(it_source):
            file_list.append(it_source)
        elif os.path.isdir(it_source):
            file_list.extend(extractFilesFromSourceDir(it_source, args.recursive))
        else:
            raise Exception(f'Unknown source : {it_source}')

    return file_list

if __name__ == '__main__':
  main()
