import {Map, List} from 'immutable';
import * as actions from 'actions';
import {PostStore} from 'PostStore'; 

const initialState = Map({
  counter: 0,
  post_store: new PostStore(),
  focused: undefined
});

const actionsMap = {
  // N.B. [x] just means it uses the value of the variable "x" as the key in the map,
  // instead of the string "x".

  [actions.TEST_ACTION]: (state) => {
    return state.merge(Map({
      counter: state.get('counter') + 1
    }));
  },

  [actions.ADD_ROOT]: (state, action) => {
    return state.set('post_store', state.get('post_store').addRootFromValues(action.post_values));
  },

  [actions.ADD_POST]: (state, action) => {
    return state.set('post_store', state.get('post_store').addChildFromValues(action.post_values));
  },

  [actions.ADD_TREE]: (state, action) => {
    return state.set('post_store', state.get('post_store').addTreeFromValues(action.posts_values));
  },

  [actions.FOCUS_POST]: (state, action) => {
    return state.set('focused', action.post_id);
  },
};

export default function reducer(state = initialState, action = {}) {
  const fn = actionsMap[action.type];
  return fn ? fn(state, action) : state;
}
