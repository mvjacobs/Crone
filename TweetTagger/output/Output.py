__author__ = 'marc'

import json
from bson import json_util


def to_json(list_of_objects, file_path='myfile.json'):
    with open(file_path, 'wb') as outfile:
        json.dump(list_of_objects, outfile, default=json_util.default)