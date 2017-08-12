export const TEST_ACTION = 'TEST_ACTION';
export const ADD_POST = 'ADD_POST';
export const SET_POSTS = 'SET_POSTS';

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
  }
}
