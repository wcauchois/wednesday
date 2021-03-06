import React, {Component} from 'react';
import {connect} from 'react-redux';

import Post from './Post';


class PostTreeComponent extends Component {
  render() {
    const sorted = this.props.root.children.sort(
      (a, b) => a.created - b.created
    );
    return <div className="post-node">
      <Post post={this.props.root} />
      {sorted.map((child, id) =>
        <PostTreeComponent key={id} root={child} /> 
      )}
    </div>;
  }
}

const PostTree = connect()(PostTreeComponent);

export default PostTree;
