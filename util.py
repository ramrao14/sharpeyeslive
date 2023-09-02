import json

def jinja_to_dict(str_dict):
  return json.loads(str_dict.replace('\'', '\"'))
