
import logging

from db import get_connection
from run_history import start_run,mark_run_success,mark_run_failed

from extract import extract
from validate import validate
from load import load

logging.basicConfig(level=logging.INFO)

def main():

    conn = None
    db_run_id = None


    try:
        logging.info("Pipeline start-up...")

        conn = get_connection()
        db_run_id = start_run(conn)
        
        data = extract()
        valid_data = validate(data)
        inserted_count = load(conn,valid_data)

        db_extracted_count = len(data)
        db_valid_count = len(valid_data)
        db_invalid_count = db_extracted_count - db_valid_count
        db_inserted_count = inserted_count
        db_skipped_count = db_valid_count - inserted_count

        mark_run_success(conn,db_run_id,db_extracted_count,db_valid_count,db_invalid_count,db_inserted_count,db_skipped_count)


        logging.info(f"Records extracted : {db_extracted_count}")
        logging.info(f"Valid records : {db_valid_count}")
        logging.info(f"Invalid records : {db_invalid_count}")
        logging.info(f"Records inserted : {db_inserted_count}")
        logging.info(f"Records skipped : {db_skipped_count}")
        logging.info("Pipeline completed successfully.")

    except Exception as e:

        if conn is not None and db_run_id is not None:
            mark_run_failed(conn,db_run_id,str(e))

        logging.error(f"Error during pipeline launch : {e}")
        raise

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()