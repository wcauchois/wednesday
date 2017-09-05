export const TEST_ACTION = 'TEST_ACTION';
export function testAction() {
  return {
    type: TEST_ACTION
  };
}

export const ADD_ROOT = 'ADD_ROOT';
export function addRoot(post) {
  return {
    type: ADD_ROOT,
    post_values: post_values
  };
}

export function newPost(post_values) {
  return async function(dispatch) {
    const ret = await Transport.call.add_post(post_values);
  };
}

export const ADD_POST = 'ADD_POST';
export function addPost(post_values) {
  return {
    type: ADD_POST,
    post_values: post_values
  };
}

export const ADD_TREE = 'ADD_TREE';
export function addTree(posts_values) {
  return {
    type: ADD_TREE,
    posts_values: posts_values
  };
}

export const FOCUS_POST = 'FOCUS_POST';
export function focusPost(post_id) {
  return {
    type: FOCUS_POST,
    post_id: post_id
  };
}
