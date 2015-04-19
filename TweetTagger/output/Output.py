__author__ = 'marc'

import json


def to_json(list_of_objects, file_path='myfile.json'):
    f = open(file_path, 'w')
    f.write(json.dumps(list_of_objects))
    f.close()


#def to_database()