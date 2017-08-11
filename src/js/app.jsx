import React, {Component} from 'react';
import {Route, Switch} from 'react-router-dom';
import ReactDOM from 'react-dom';
import {createStore, applyMiddleware, compose} from 'redux';
import {Provider, connect} from 'react-redux';
import thunk from 'redux-thunk';
import {Map} from 'immutable';
import Root from 'views/Root';

import '../less/styles.less';

const initialState = Map({
  counter: 0
});

const TEST_ACTION = 'TEST_ACTION';

const actionsMap = {
  [TEST_ACTION]: (state) => {
    return state.merge(Map({
      counter: state.get('counter') + 1
    }));
  }
};

function rootReducer(state = initialState, action = {}) {
  const fn = actionsMap[action.type];
  return fn ? fn(state, action) : state;
}

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

/*
class ThingComponent extends Component {
  render() {
    return <div>
      <div>hi i'm a counter, my value is: <strong>{this.props.counter}</strong></div>
      <div>
        <button onClick={this.props.onButtonClicked}>click me</button>
      </div>
    </div>;
  }
}
const Thing = connect(
  state => {
    return {
      counter: state.get('counter')
    };
  },
  dispatch => {
    return {
      onButtonClicked: () => dispatch({type: TEST_ACTION})
    }
  }
)(ThingComponent);

class Index extends Component {
  render() {
    return <div>
      <h1>
        jesus fuck this took a while
      </h1>
      <div>
        <Thing />
      </div>
    </div>;
  }
}
*/

ReactDOM.render(
  <Provider store={store}>
    <Root />
  </Provider>,
  document.getElementById('root')
);
