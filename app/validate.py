
from db import get_required_env
from pathlib import Path

import json
import logging

logging.basicConfig(level=logging.INFO)

def validate(data):
    valid_data = []
    dlq_data = []
    keys = ['userId', 'id', 'title', 'body']
    types = [int,int,str,str]
    dlq_file = get_required_env("DLQ_PATH")
    dlq_file_path = Path(dlq_file)
    dlq_file_path.parent.mkdir(parents=True, exist_ok=True)

    for record in data :
        errors = []
        missed_keys = []
        record_id = record.get("id", "UNKNOWN")
        for key in keys:
            if key not in record:
                missed_keys.append(key)
                error = f"Error record[{record_id}] | missing field({key})"
                errors.append(error)
        
        for idx, key in enumerate(keys):
            if key not in missed_keys :
                if not(isinstance(record[key], types[idx])):
                    error = f"Error record[{record_id}] | invalid type | field({key}) : expected type({types[idx].__name__}) != type received({type(record[key]).__name__})"
                    errors.append(error)
        
        if 'userId' not in missed_keys and isinstance(record['userId'], int):
            if record['userId'] <= 0 :
                error = f"Error record[{record_id}] | userId must be strictly positive"
                errors.append(error)
        
        if 'title' not in missed_keys and isinstance(record['title'], str):
            if record['title'].strip() == "" :
                error = f"Error record[{record_id}] | title must contain something"
                errors.append(error)
            
        if len(errors) == 0 :
            valid_data.append(record)
        else:
            dlq = {"record": record, "errors": errors}
            dlq_data.append(dlq)
    
    with open(dlq_file_path,"w") as f:
        for dlq in dlq_data:
            f.write(json.dumps(dlq) + "\n")

    logging.info(f"number of records = {len(data)}")
    logging.info(f"number of valid records = {len(valid_data)}")
    logging.info(f"number of rejected records = {len(dlq_data)}")


                

    return valid_data