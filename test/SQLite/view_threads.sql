SELECT ac.depth, ac.body as 'First', bc.body as 'Second', cc.body as 'Third', s.label
FROM comments as ac, comments as bc, comments as cc, submissions as s
WHERE ac.submission_id = bc.submission_id
AND bc.submission_id = cc.submission_id
and cc.submission_id = s.submission_id
AND s.submission_id = '6f70nk'
AND ac.comment_id = bc.parent_id
AND bc.comment_id = cc.parent_id
AND (ac.depth = 0
OR ac.depth = 1)

ORDER BY ac.depth