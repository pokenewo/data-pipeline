

def start_run(conn):
    with conn.cursor() as cur:
        cur.execute("""
            insert into run_history (status)
            values ('RUNNING')
            returning run_id;
        """)
        run_id = cur.fetchone()[0]

        conn.commit()
        return run_id



def mark_run_success(conn,run_id,extracted_count,valid_count,invalid_count,inserted_count,skipped_count):
    update_query ="""
        update run_history 
        set
            ended_at = current_timestamp, 
            status = 'SUCCESS', 
            extracted_count = %s, 
            valid_count = %s, 
            invalid_count = %s, 
            inserted_count = %s, 
            skipped_count = %s 
        where run_id = %s;
    """
    with conn.cursor() as cur:
        values = (extracted_count,valid_count,invalid_count,inserted_count,skipped_count,run_id)
        cur.execute(update_query,values)

        conn.commit()



def mark_run_failed(conn, run_id,error_message):
    update_query ="""
        update run_history 
        set
            ended_at = current_timestamp, 
            status = 'FAILED', 
            error_message = %s 
        where run_id = %s;
    """
    with conn.cursor() as cur:
        values = (error_message,run_id)
        cur.execute(update_query,values)

        conn.commit()