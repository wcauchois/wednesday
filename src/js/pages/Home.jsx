import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {addPost, setPosts} from 'actions';
import Transport from 'Transport';

class Post extends Component {
  render() {
    return <div className="post">
      <div className="post-inner">
        <div className="title">
          <span className="author">
            Anonymous
          </span>
        </div>
        <div className="content">
          {this.props.post.content}
        </div>
      </div>
    </div>
  }
}

class AddPostComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {content: ''};
  }

  handleTextareaChange(event) {
    this.setState({content: event.target.value});
  }

  submitButtonClicked() {
    if (this.state.content) {
      this.props.addPost({
        content: this.state.content
      });
      this.setState({content: ''});
    }
  }

  render() {
    return <div className="add-post">
      <div className="textarea">
        <textarea value={this.state.content} onChange={this.handleTextareaChange.bind(this)} />
      </div>
      <div className="controls">
        <button onClick={this.submitButtonClicked.bind(this)}>Add Post</button>
      </div>
    </div>;
  }
}

const AddPost = connect(
  null,
  dispatch => {
    return {
      addPost: post => {
        dispatch(async function(dispatch) {
          const postFromServer = await Transport.call.add_post(post);
          dispatch(addPost(postFromServer));
        });
      }
    };
  }
)(AddPostComponent);

class PostListComponent extends Component {
  render() {
    const posts = this.props.posts.map((post, index) => {
      return <Post key={index} post={post} />;
    });
    return <div>
      {posts}
      <AddPost />
    </div>;
  }
}

const PostList = connect(
  state => {
    return {posts: state.get('posts')};
  }
)(PostListComponent);

class HomeComponent extends Component {
  render() {
    return <div>
      This is the index page.<br />
      <Link to="/about">About page</Link><br />
      <div>
        <PostList />
      </div>
    </div>;
  }

  componentDidMount() {
    this.props.loadPosts();
  }
}

const Home = connect(
  null,
  dispatch => {
    return {
      loadPosts: () => {
        dispatch(async function(dispatch) {
          const response = await Transport.call.all_posts();
          dispatch(setPosts(response.posts));
        });
      }
    };
  }
)(HomeComponent);

export default Home;
