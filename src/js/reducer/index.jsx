import {Map, List} from 'immutable';
import * as actions from 'actions';
import {PostStore} from 'PostStore'; 

const initialState = Map({
  counter: 0,
  post_store: new PostStore(),
  focused: undefined,
  timestamp: new Date().getTime(),
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

  [actions.UPDATE_TIME]: (state, action) => {
    return state.set('timestamp', action.timestamp);
  },

  [actions.MOVE_FOCUS]: (state, action) => {
    const currentFocus = state.get('focused');
    const postStore = state.get('post_store');
    const delta = action.delta;
    let newFocus = currentFocus;
    if (currentFocus) {
      // NOTE(wcauchois): This is a pretty inefficient algorithm that flattens the whole tree.
      // Might be able to come up with something better...
      const linearView = [];
      for (const [_, root] of postStore.roots) {
        for (const node of root.flatView()) {
          linearView.push(node.id);
        }
      }
      const currentIndex = linearView.indexOf(currentFocus);
      const newIndex = Math.min(Math.max(currentIndex + delta, 0), linearView.length - 1);
      newFocus = linearView[newIndex];
    } else {
      if (postStore.roots.size > 0) {
        newFocus = postStore.roots.first().id;
      }
    }
    return state.set('focused', newFocus);
  },
};

export default function reducer(state = initialState, action = {}) {
  const fn = actionsMap[action.type];
  return fn ? fn(state, action) : state;
}
