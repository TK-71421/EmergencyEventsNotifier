SELECT DISTINCT
    tp.title as twitter, tp.date_posted, rp.title as reddit, rp.created_utc
FROM
    twitter_posts tp
JOIN
    reddit_posts rp ON
    (
        LOWER(tp.title) LIKE CONCAT('%', rp.title, '%')
        OR LOWER(rp.title) LIKE CONCAT('%', tp.title, '%')
    )
WHERE
    LOWER(tp.title) LIKE '%gaza%'
    AND LOWER(tp.title) LIKE '%injured%'
    AND LOWER(tp.title) LIKE '% in %'
    AND (
        LOWER(tp.title) LIKE '%airstrike%'
        OR LOWER(tp.title) LIKE '%bomb%'
        OR LOWER(tp.title) LIKE '%hospital%'
        OR LOWER(tp.title) LIKE '%raid%'
    );