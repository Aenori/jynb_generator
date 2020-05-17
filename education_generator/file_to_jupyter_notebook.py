from enum import Enum
import json
import logging
import os

logger = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

DEFAULT_METADATA_FILE = f'{dir_path}/jynb_metadata.json'
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
    UNITTEST = 3
    EXERCICE_PLACEHOLDER = 4

TAG_TO_TYPE = {
    'Correction' : CellType.CORRECTION,
    'Test unitaire' : CellType.UNITTEST,
    'Exercice placeholder' : CellType.EXERCICE_PLACEHOLDER,
}

class FileToJupyterNotebook:
    def __init__(self, write_unittest_file = False, correction_mode = False, metadata_file = DEFAULT_METADATA_FILE):
        self.metadata_file = metadata_file
        self.write_unittest_file = write_unittest_file
        self.correction_mode = correction_mode

    def convertFileListToNotebook(self, file_list, output):
        cell_list = []
        tu_list = []

        for it_file in file_list:
            it_cell_list, it_tu_list = self.__convertFileToCells(it_file)
            cell_list.extend(it_cell_list)
            tu_list.extend(it_tu_list)

        with open(self.metadata_file, 'r') as f:
            json_data = json.load(f)
            json_data['cells'] = cell_list

        with open(output, 'w') as output_f:
            output_f.write(json.dumps(json_data, indent=2, sort_keys=True))

    def __convertFileToCells(self, source_file):
        cell_list_raw = self.__extractCellsFromSourceFile(source_file)

        unittest_codes = list(filter(lambda x : x['type'] == CellType.UNITTEST, cell_list_raw))
        cell_list_nb_raw = list(filter(self.__includeCellInNotebook, cell_list_raw))

        return [self.__convertRawToJupyter(it_raw_cell) for it_raw_cell in cell_list_nb_raw], unittest_codes

    def __includeCellInNotebook(self, it_raw_cell):
        print((self.correction_mode, it_raw_cell['type']))

        if it_raw_cell['type'] == CellType.UNITTEST:
            return False
            
        if self.correction_mode:
            return it_raw_cell['type'] != CellType.EXERCICE_PLACEHOLDER
        else:
            return it_raw_cell['type'] != CellType.CORRECTION

    def __convertRawToJupyter(self, it_raw_cell):
        jupyter_cell = JUPYTER_NOTEBOOK_TEMPLATE.copy()
        
        if it_raw_cell['type'] == CellType.MARKDOWN:
            jupyter_cell['cell_type'] = 'markdown'
        else:
            jupyter_cell['cell_type'] = 'code'
            jupyter_cell['outputs'] = []
            jupyter_cell['execution_count'] = None

        jupyter_cell['source'] = it_raw_cell['source']
      
        return jupyter_cell  

    def __extractCellsFromSourceFile(self, source_file):
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

                    current_cell_type = self.__findCurrentCelltype(it_line, current_cell_type)
                    
                    logger.debug(f"Line {it_line_number} => {current_cell_type}")
                else:
                    current_cell_source.append(it_line)

        if len(current_cell_source) != 0:
            cell_list.append({'type' : current_cell_type, 'source' : current_cell_source})

        return cell_list

    def __findCurrentCelltype(self, line, current_cell_type):
        if line.startswith('~~~ #'):
            assert(current_cell_type == CellType.MARKDOWN)
            cell_type = line[5:].strip()
            current_cell_type = TAG_TO_TYPE[cell_type]
        elif current_cell_type == CellType.MARKDOWN:
            current_cell_type = CellType.CODE
        else:
            current_cell_type = CellType.MARKDOWN

        return current_cell_type
