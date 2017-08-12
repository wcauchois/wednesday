export const TEST_ACTION = 'TEST_ACTION';
export const ADD_POST = 'ADD_POST';

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
