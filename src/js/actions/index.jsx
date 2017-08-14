export const TEST_ACTION = 'TEST_ACTION';
export const ADD_POST = 'ADD_POST'; // DEPRECATED ?
export const SET_POSTS = 'SET_POSTS'; // DEPRECATED ?
export const SET_POST_GRAPH = 'SET_POST_GRAPH';
export const UPDATE_POST_GRAPH = 'UPDATE_POST_GRAPH';
export const FOCUS_POST = 'FOCUS_POST';


export function testAction() {
  return {
    type: TEST_ACTION
  };
}

export function addPost(post) {
  return {
    type: ADD_POST,
    post: post
  };
}

export function setPosts(posts) {
  return {
    type: SET_POSTS,
    posts: posts
  };
}

export function setPostGraph(graph) {
  return {
    type: SET_POST_GRAPH,
    graph: graph
  };
}

export function updatePostGraph(ops) {
  return {
    type: UPDATE_POST_GRAPH,
    ops: ops
  };
}

export function focusPost(post_id) {
  return {
    type: FOCUS_POST,
    post_id: post_id
  };
}
