import logging
from extract import extract
from validate import validate
from load import load

logging.basicConfig(level=logging.INFO)

def main():
    try:
        logging.info("Pipeline start-up...")
        data = extract()
        valid_data = validate(data)
        inserted_count = load(valid_data)

        logging.info(f"Records extracted : {len(data)}")
        logging.info(f"Valid records : {len(valid_data)}")
        logging.info(f"Records inserted : {inserted_count}")
        logging.info("Pipeline completed successfully.")

    except Exception as e:
        logging.error(f"Error during pipeline launch : {e}")
        raise


if __name__ == "__main__":
    main()