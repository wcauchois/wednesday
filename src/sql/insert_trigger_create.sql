CREATE OR REPLACE FUNCTION notify_post_inserted()
  RETURNS trigger AS $$
DECLARE
  cur posts%ROWTYPE;
BEGIN
  cur = NEW;
  WHILE cur.id > 0 LOOP
    PERFORM pg_notify(
      CAST(('pubsub_' || cur.parent_id) AS text),
      row_to_json(NEW)::text);
    SELECT * INTO cur FROM posts WHERE id = cur.parent_id;
  END LOOP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS notify_post_inserted ON posts;
CREATE TRIGGER notify_post_inserted
  AFTER INSERT ON posts
  FOR EACH ROW
  EXECUTE PROCEDURE notify_post_inserted();
