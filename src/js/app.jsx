import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import Root from 'views/Root';
import Transport from 'Transport';
import store from 'config/store';
import '../less/styles.less';

// Convenience aliases for the JavaScript console
global.Transport = Transport;
global.store = store;

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
