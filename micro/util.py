import json
from logger import log

def to_json(value: str):
    try:        
        log.info(f"to_json before {value}") 
        json_value = json.loads(value)
        log.info(f"to_json after {json_value}") 
        return json_value
    except json.JSONDecodeError as ex:
        log.error(f"JSONDecodeError with value {value} - {ex}")
        return None