CREATE OR REPLACE FUNCTION subtree(parent integer, max_depth integer)
RETURNS SETOF posts AS
$$
  WITH RECURSIVE subtree(id, created, parent_id, content, ip_address, depth) AS (
      SELECT p.id, p.created, p.parent_id, p.content, p.ip_address, 1
      FROM posts p WHERE p.id = parent
    UNION ALL
      SELECT p.id, p.created, p.parent_id, p.content, p.ip_address, st.depth + 1
      FROM posts p, subtree st
      WHERE p.parent_id = st.id AND st.depth < max_depth
  )
  SELECT st.id, st.created, st.parent_id, st.content, st.ip_address FROM subtree st;
$$
LANGUAGE SQL;
