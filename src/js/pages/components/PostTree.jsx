import React, {Component} from 'react';
import {connect} from 'react-redux';

import Post from './Post';


class PostTreeComponent extends Component {
  render() {
    return <div className="post-node">
      <Post post={this.props.root} />
      {this.props.root.children.map((child, id) =>
        <PostTreeComponent key={id} root={child} /> 
      )}
    </div>;
  }
}

const PostTree = connect()(PostTreeComponent);

export default PostTree;
