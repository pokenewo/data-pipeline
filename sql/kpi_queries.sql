-- ============================================================
-- KPI Queries
-- Source : clean_posts
-- Description :
--   These queries provide simple analytical indicators from the
--   cleaned posts dataset.
-- ============================================================

-- KPI 1 : Combien de posts chaque utilisateur possède-t-il ?
select
    user_id,
    count(*) as total_posts
from clean_posts
group by user_id
order by user_id;


-- KPI 2 : Quelle est la longueur moyenne des titres par utilisateur ?
select
    user_id,
    round(avg(title_length), 2) as avg_title_length
from clean_posts
group by user_id
order by user_id;


-- KPI 3 : Quels utilisateurs ont une longueur moyenne de titre supérieure à 40 caractères ?
select
    user_id,
    round(avg(title_length), 2) as avg_title_length
from clean_posts
group by user_id
having avg(title_length) > 40
order by avg_title_length desc;


-- KPI 4 : Quels utilisateurs ont produit le plus de contenu en volume de texte ?
select
    user_id,
    sum(body_length) as total_content_length
from clean_posts
group by user_id
order by total_content_length desc;


-- KPI 5 : Quels sont les posts les plus longs, classés du plus long au plus court ?
select
    post_id,
    user_id,
    body_length,
    rank() over (
        order by body_length desc
    ) as body_length_rank
from clean_posts
order by body_length_rank
limit 10;


-- KPI 6 : Classer les posts de chaque utilisateur du plus long au plus court
select
    post_id,
    user_id,
    body_length,
    rank() over (
        partition by user_id
        order by body_length desc
    ) as rank_within_user
from clean_posts
order by user_id, rank_within_user;