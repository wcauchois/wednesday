import React, {Component} from 'react';
import {connect} from 'react-redux';


class PostPreviewListComponent extends Component {
  render() {
    return <div className="post-preview-list">
      <span className="grid-column-header">{"HOT"}</span>
      {this.props.posts.map((post) =>
        // (amstocker) should be replaced with a PostPreview component eventually...
        <Post post={post} key={post.id} />
      )}
    </div>;
  }
}

const PostPreviewList = connect(
  state => {
    return {
      posts: state.get('hot_posts')
    };
  }
)(PostPreviewListComponent);

export default PostPreviewList;
