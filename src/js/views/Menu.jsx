import React, {Component} from 'react';
import {Link} from 'react-router-dom';

const menuEntries = [
  ['/', 'Home'],
  ['/about', 'About']
];

export default class Menu extends Component {
  render() {
    const entries = menuEntries.map(([path, text], index) => {
      return <Link to={path} key={index}>
        <li>
          {text}
        </li>
      </Link>;
    });
    return <div className="menu">
      <div className="nav">
        <ul>
          {entries}
        </ul>
      </div>
    </div>;
  }
}
