CREATE OR REPLACE FUNCTION update_subtree_scores()
  RETURNS trigger AS $$
BEGIN
  -- (amstocker) for now, this just updates all scores upon insert
  
  PERFORM score_trigger_helper(posts.*) FROM posts WHERE parent_id is NULL;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
