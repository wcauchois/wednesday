CREATE OR REPLACE FUNCTION post_score2(post posts) RETURNS real AS
$$
BEGIN
  -- score = (K*ln(# of child posts)/(now() - post.created) - post.parent.score
  --
  -- Notes:
  --  -) K is some scaling constant
  --  -) Can't take LN() of zero so just use some small number
  --  -) Minimum dt is 1 second to avoid division by zero
  --  -) If post has no parent, don't subtract anything
  RETURN (3600 * LN(GREATEST(1e-37, (SELECT count(*) FROM posts WHERE parent_id=post.id))) 
            / GREATEST(extract(epoch from (now()-post.created)), 1))
         - coalesce((SELECT score from posts where id=post.parent_id), 0);
END;
$$
LANGUAGE 'plpgsql';
