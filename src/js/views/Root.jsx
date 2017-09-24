import React, {Component, PropTypes} from 'react';
import {BrowserRouter} from 'react-router-dom';
import Routes from 'config/routes';
import Menu from 'views/Menu';
import keymap from 'keymap';
import {ShortcutManager} from 'react-shortcuts';

const shortcutManager = new ShortcutManager(keymap);

export default class Root extends Component {
  getChildContext() {
    return {
      shortcuts: shortcutManager,
    };
  }

  render() {
    return <BrowserRouter>
      <div className="app">
        <div className="page">
          <Routes />
        </div>
      </div>
    </BrowserRouter>;
  }
}

Root.childContextTypes = {
  shortcuts: PropTypes.object.isRequired,
};
