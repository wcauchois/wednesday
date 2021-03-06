export const TEST_ACTION = 'TEST_ACTION';
export function testAction() {
  return {
    type: TEST_ACTION
  };
}

export const ADD_ROOT = 'ADD_ROOT';
// XXX(wcauchois): Is this used?
export function addRoot(post_values) {
  return {
    type: ADD_ROOT,
    post_values
  };
}

export function newPost(post_values) {
  return async function(dispatch) {
    const ret = await Transport.call.addPost(post_values);
  };
}

export const ADD_POST = 'ADD_POST';
export function addPost(post_values) {
  return {
    type: ADD_POST,
    post_values: post_values,
  };
}

export const ADD_TREE = 'ADD_TREE';
export function addTree(posts_values) {
  return {
    type: ADD_TREE,
    posts_values,
  };
}

export const HOT_POSTS_SET_INTERVAL = 'HOT_POSTS_SET_INTERVAL';
export function hotPostsSetInterval(id) {
  return {
    type: HOT_POSTS_SET_INTERVAL,
    id,
  };
}

export const HOT_POSTS_STOP_INTERVAL = 'HOT_POSTS_STOP_INTERVAL';
export function hotPostsStopInterval() {
  return {
    type: HOT_POSTS_STOP_INTERVAL,
  };
}

export const HOT_POSTS_SET = 'HOT_POSTS_SET';
export function hotPostsSet(posts_values) {
  return {
    type: HOT_POSTS_SET,
    posts_values,
  };
}

export function hotPostsPoll(interval) {
  return function(dispatch) {
    // should prob impl some kind of timeout behavior
    const id = setInterval(() => {
      Transport.call.getHot({n: 10}).then((ret) => {
        dispatch(hotPostsSet(ret));
      });
    }, interval);
    dispatch(hotPostsSetInterval(id));
  };
}

export const FOCUS_POST = 'FOCUS_POST';
export function focusPost(post_id) {
  return {
    type: FOCUS_POST,
    post_id,
  };
}

export const UPDATE_TIME = 'UPDATE_TIME';
export function updateTime(timestamp) {
  return {
    type: UPDATE_TIME,
    timestamp,
  };
}

export const MOVE_FOCUS = 'MOVE_FOCUS';
export function moveFocus(delta) {
  return {
    type: MOVE_FOCUS,
    delta,
  };
}

export const SET_ADD_POST_MARGIN_LEFT = 'SET_ADD_POST_MARGIN_LEFT';
export function setAddPostMarginLeft(value) {
  return {
    type: SET_ADD_POST_MARGIN_LEFT,
    value
  };
}
