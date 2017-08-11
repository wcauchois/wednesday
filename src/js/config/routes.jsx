import React from 'react';
import {Route, Switch} from 'react-router-dom';
import Index from 'pages/Index';
import About from 'pages/About';

const publicPath = '/';

export default () => (
  <Switch>
    <Route exact path='/' component={Index} />
    <Route path='/about' component={About} />
  </Switch>
);
