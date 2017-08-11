import React, {Component} from 'react';
import {Link} from 'react-router-dom';

class Post extends Component {
  render() {
    return <div className="post">
      <div className="post-inner">
        <div className="title">
          <span className="author">
            {this.props.author}
          </span>
        </div>
        <div className="content">
          {this.props.text}
        </div>
      </div>
    </div>
  }
}

export default class Index extends Component {
  render() {
    return <div>
      This is the index page.<br />
      <Link to="/about">About page</Link><br />
      <div>
        <Post author="Andrew" text="Hi my name is andrew" />
        <Post author="Bill" text="Bill bill bill bill bill bill" />
      </div>
    </div>;
  }
}
