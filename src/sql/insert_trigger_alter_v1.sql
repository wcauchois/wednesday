CREATE OR REPLACE FUNCTION notify_post_inserted()
  RETURNS trigger AS $$
DECLARE
  cur posts%ROWTYPE;
BEGIN
  cur = NEW;
  WHILE cur.id > 0 AND cur.parent_id IS NOT NULL LOOP
    PERFORM pg_notify(
      CAST(('pubsub_' || cur.parent_id) AS text),
      row_to_json(NEW)::text);
    SELECT * INTO cur FROM posts WHERE id = cur.parent_id;
  END LOOP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
