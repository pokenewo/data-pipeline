import psycopg2
import logging

logging.basicConfig(level=logging.INFO)



def load(valid_data):
    
    inserted_count = 0
    skipped_count = 0
    insert_query = """ INSERT INTO staging_posts (user_id,post_id,title,body) VALUES (%s,%s,%s,%s) ON CONFLICT (post_id) DO NOTHING"""

    try:
        logging.info("Chargement en cours...")
        with psycopg2.connect(
            dbname="pipeline_db",
            user="willo",
            password="newoXsuzy2008",
            host="localhost",
            port="5432"
        ) as conn:
            with conn.cursor() as cur:
                for record in valid_data:
                    values = (record['userId'], record['id'], record['title'], record['body'])

                    cur.execute(insert_query,values)
                    if cur.rowcount == 1:
                        inserted_count += 1
                    else:
                        skipped_count += 1

                conn.commit()
                logging.info(f"Records inserted: {inserted_count}") 
                logging.info(f"Records skipped: {skipped_count}")


    except psycopg2.Error as e:
        logging.error(f"Erreur lors du chargement : {e}")
        raise

    return inserted_count

