CREATE OR REPLACE FUNCTION score_trigger_helper(post posts) RETURNS void AS
$$
DECLARE
  iter_row posts%ROWTYPE;
BEGIN
  UPDATE posts SET score = post_score2(posts.*) WHERE id = post.id;
  PERFORM score_trigger_helper(posts.*) FROM posts WHERE parent_id = post.id;
END;
$$
LANGUAGE 'plpgsql';
