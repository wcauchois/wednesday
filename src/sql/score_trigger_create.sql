CREATE OR REPLACE FUNCTION update_subtree_scores()
  RETURNS trigger AS $$
BEGIN
  -- (amstocker) for now, this just updates all scores upon insert
  UPDATE posts SET score = post_score(posts.*);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_subtree_scores ON posts;
CREATE TRIGGER update_subtree_scores
  AFTER INSERT ON posts
  FOR EACH ROW
  EXECUTE PROCEDURE update_subtree_scores();
