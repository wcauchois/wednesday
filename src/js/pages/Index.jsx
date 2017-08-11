import React, {Component} from 'react';
import {Link} from 'react-router-dom';

export default class Index extends Component {
  render() {
    return <div>
      This is the index page.<br />
      <Link to="/about">About page</Link>
    </div>;
  }
}
