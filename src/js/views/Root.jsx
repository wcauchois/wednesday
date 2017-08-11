import React, {Component} from 'react';
import {BrowserRouter} from 'react-router-dom';
import Routes from 'config/routes';
import Menu from 'views/Menu';

export default class Root extends Component {
  render() {
    return <BrowserRouter>
      <div className="app">
        <Menu />
        <div className="page">
          <Routes />
        </div>
      </div>
    </BrowserRouter>;
  }
}
