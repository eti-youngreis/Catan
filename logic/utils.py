import json
import re
import traceback


def load_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print('Error in load_config ', e)


def print_error(class_name='', function_name='', e=Exception()):
    print('Error in', class_name, function_name, "line", e.__traceback__.tb_lineno, ":", e)


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def get_key_by_value(dic: dict, val) -> str:
    try:
        try:
            val = int(val)
        except (ValueError, TypeError):
            pass
        return [key for key in dic.keys() if dic[key] == val][0]
    except (IndexError, KeyError):
        print(traceback.format_exc())
