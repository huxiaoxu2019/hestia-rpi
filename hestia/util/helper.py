import json
def isJson(msg):
    try:
        json.loads(msg)
    except ValueError:
        return False
    return True
