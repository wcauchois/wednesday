CREATE OR REPLACE FUNCTION post_score2(post posts) RETURNS real AS
$$
DECLARE
  nchild integer;
BEGIN
  -- score = exp(ln(# of child posts)/dt) / parent.score
  
  SELECT INTO nchild count(*) FROM posts WHERE parent_id=post.id;
  IF nchild > 0 THEN
    -- can rescale time (e.g. here 300 is on the scale of 5 min)
    RETURN EXP((300 * LN(nchild)) / GREATEST(extract(epoch from (now()-post.created)), 1))
            / coalesce((SELECT score from posts where id=post.parent_id), 1);
  ELSE
    RETURN 0;
  END IF;
END;
$$
LANGUAGE 'plpgsql';
