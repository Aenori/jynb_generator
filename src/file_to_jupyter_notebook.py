from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)

DEFAULT_METADATA_FILE = 'src/jynb_metadata.json'
TO_BE_MODIFIED = None

JUPYTER_NOTEBOOK_TEMPLATE =   {
    "cell_type": TO_BE_MODIFIED,
    "metadata": {}, 
    "source": TO_BE_MODIFIED
}

class CellType(Enum):
    MARKDOWN = 0
    CODE = 1
    CORRECTION = 2

def convertFileListToNotebook(file_list, output, metadata_file=DEFAULT_METADATA_FILE):
    cell_list = []

    for it_file in file_list:
        cell_list.extend(_convertFileToCells(it_file))

    with open(metadata_file, 'r') as f:
        json_data = json.load(f)
        json_data['cells'] = cell_list

    with open(output, 'w') as output_f:
        output_f.write(json.dumps(json_data, indent=2, sort_keys=True))

def _convertFileToCells(source_file):
    cell_list_raw = _extractCellsFromSourceFile(source_file)
    return [_convertRawToJupyter(it_raw_cell) for it_raw_cell in cell_list_raw]

def _convertRawToJupyter(it_raw_cell):
    jupyter_cell = JUPYTER_NOTEBOOK_TEMPLATE.copy()
    
    if it_raw_cell['type'] == CellType.MARKDOWN:
        jupyter_cell['cell_type'] = 'markdown'
    else:
        jupyter_cell['cell_type'] = 'code'
        jupyter_cell['outputs'] = []
        jupyter_cell['execution_count'] = None


    jupyter_cell['source'] = it_raw_cell['source']
  
    return jupyter_cell  

def _extractCellsFromSourceFile(source_file):
    cell_list = []
  
    current_cell_type = CellType.MARKDOWN
    current_cell_source = []

    with open(source_file, 'r') as f:
        for it_line_number, it_line in enumerate(f):
            if (it_line_number < 3) and it_line.startswith('%'):
                continue
  
      # trigger to change cell type
        if it_line.startswith('~~~'):
            cell_list.append({'type' : current_cell_type, 'source' : current_cell_source})
            current_cell_source = []

            if it_line.startswith('~~~ # Correction'):
                assert(current_cell_type == CellType.MARKDOWN)
                current_cell_type = CellType.CORRECTION
            elif current_cell_type == CellType.MARKDOWN:
                current_cell_type = CellType.CODE
            else:
                current_cell_type = CellType.MARKDOWN
            
            logger.debug(f"Line {it_line_number} => {current_cell_type}")
        else:
            current_cell_source.append(it_line)

    if len(current_cell_source) != 0:
        cell_list.append({'type' : current_cell_type, 'source' : current_cell_source})

    return cell_list