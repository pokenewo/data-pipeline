
drop table if exists staging_posts;
create table staging_posts (
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
