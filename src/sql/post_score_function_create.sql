CREATE OR REPLACE FUNCTION post_score(post posts) RETURNS real AS
$$
BEGIN
  -- score = (# of child posts)/(now - post.created) - parent.score
  
  RETURN 100000*(select count(*) from posts where parent_id=post.id)
            /GREATEST(extract(epoch from (now()-post.created)), 1)
         - coalesce((SELECT score from posts where id=post.parent_id), 0);
END;
$$
LANGUAGE 'plpgsql';
