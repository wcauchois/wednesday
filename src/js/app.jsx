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

ReactDOM.render(
  <Provider store={store}>
    <Root />
  </Provider>,
  document.getElementById('root')
);
