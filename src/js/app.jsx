import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import Root from 'views/Root';
import Transport from 'Transport';
import store from 'config/store';
import * as actions from 'actions';
import '../less/styles.less';

// Convenience aliases for the JavaScript console
global.Transport = Transport;
global.store = store;

Transport.on('sub_new_post', (payload) => {
  store.dispatch(actions.addPost(payload.post));
});

setInterval(() => {
  store.dispatch(actions.updateTime(new Date().getTime()));
}, 1000);

ReactDOM.render(
  <Provider store={store}>
    <Root />
  </Provider>,
  document.getElementById('root')
);
