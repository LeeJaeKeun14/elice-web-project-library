import json
import os
from pathlib import Path

DIR_PATH = os.getcwd()
file_path = Path(str(Path(DIR_PATH).parent) + "\Applications_info.json")

json_data = {
    "mysql" : {
        "id" : "",
        "pw" : ""
    }
}

with open(file_path, 'w', encoding='utf-8') as make_file:
    json.dump(json_data, make_file, indent="\t")