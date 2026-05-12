-- ============================================================
-- Transformations SQL
-- Source : staging_posts
-- Target : clean_posts
-- Description :
--   This script creates a clean analytical table from raw/staging
--   API data. It keeps only valid records and adds simple derived
--   columns useful for KPI queries.
-- ============================================================
drop table if exists clean_posts;


create table clean_posts as
select
    post_id,
    user_id,
    trim(title) as title,
    trim(body) as body,
    length(trim(title)) as title_length,
    length(trim(body)) as body_length
from staging_posts
where title is not null
 and trim(title) <> ''
 and user_id > 0;