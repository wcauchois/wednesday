import {TEST_ACTION, ADD_POST, SET_POSTS, SET_POST_GRAPH, UPDATE_POST_GRAPH, FOCUS_POST} from 'actions'
import {Map, List} from 'immutable';
import {GraphStore} from 'graph-store';

const initialState = Map({
  counter: 0,
  posts: List(),
  post_graph: new GraphStore(),
  focused: undefined
});

const actionsMap = {
  // N.B. [x] just means it uses the value of the variable "x" as the key in the map,
  // instead of the string "x".

  [TEST_ACTION]: (state) => {
    return state.merge(Map({
      counter: state.get('counter') + 1
    }));
  },

  [ADD_POST]: (state, action) => {
    return state.update('posts', posts => posts.push(action.post));
  },

  [SET_POSTS]: (state, action) => {
    return state.set('posts', List(action.posts));
  },

  [SET_POST_GRAPH]: (state, action) => {
    return state.set('post_graph', action.graph);
  },

  [UPDATE_POST_GRAPH]: (state, action) => {
    return state.set('post_graph', state.get('post_graph').apply(action.ops));
  },

  [FOCUS_POST]: (state, action) => {
    console.log(action.post_id);
    return state.set('focused', action.post_id);
  },
};

export default function reducer(state = initialState, action = {}) {
  const fn = actionsMap[action.type];
  return fn ? fn(state, action) : state;
}
