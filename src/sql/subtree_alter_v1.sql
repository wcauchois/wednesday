CREATE OR REPLACE FUNCTION subtree(parent integer, max_depth integer)
RETURNS SETOF posts AS
$$
  WITH RECURSIVE subtree AS (
      SELECT *
      FROM posts p WHERE p.id = parent
    UNION ALL
      SELECT p.*
      FROM posts p, subtree st
      WHERE p.parent_id = st.id
  )
  SELECT * FROM subtree st limit max_depth;
$$
LANGUAGE SQL;
