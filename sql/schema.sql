
create table if not exists staging_posts (
    post_id int not null,
    user_id int not null,
    title text not null,
    body text not null,

    constraint pk_staging_posts primary key (post_id),
    constraint chk_valid_userid check(user_id > 0),
    constraint chk_valid_title check(title != '')
);

-- ============================================================
-- Pipeline run history
-- Description :
--   Stores metadata about each pipeline execution.
-- ============================================================

create table if not exists run_history (
    run_id serial,
    started_at timestamp not null default current_timestamp,
    ended_at timestamp,
    status varchar(20) not null default 'RUNNING',
    extracted_count int not null default 0,
    valid_count int not null default 0,
    invalid_count int not null default 0,
    inserted_count int not null default 0,
    skipped_count int not null default 0,
    error_message text,

    constraint pk_run_history primary key (run_id),
    constraint chk_run_history_status check (status in ('RUNNING', 'SUCCESS', 'FAILED')),
    constraint chk_run_history_extracted_count check (extracted_count >= 0),
    constraint chk_run_history_valid_count check (valid_count >= 0),
    constraint chk_run_history_invalid_count check (invalid_count >= 0),
    constraint chk_run_history_inserted_count check (inserted_count >= 0),
    constraint chk_run_history_skipped_count check (skipped_count >= 0),
    constraint chk_run_history_load_count check (inserted_count + skipped_count <= valid_count)
    

    
);