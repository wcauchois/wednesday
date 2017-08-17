import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import {addPost, setPosts, focusPost} from 'actions';
import Transport from 'Transport';
import moment from 'moment';
import tinycolor from 'tinycolor2';
import {pickColorFromString, nbsp} from 'Utils';
import classNames from 'classnames';


class PostComponent extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.focusPost(this.props.post.id);
  }

  render() {
    const created = moment.unix(this.props.post.created);
    const absoluteTimestamp = created.format('MM/DD/YY(ddd)HH:mm:ss');
    const relativeTimestamp = created.fromNow();
    let authorId;
    if (this.props.post.anonymized_author_identifier) {
      const identifier = this.props.post.anonymized_author_identifier;
      const bgColor = pickColorFromString(identifier);
      const bgTinyColor = tinycolor({r: bgColor[0], g: bgColor[1], b: bgColor[2]});
      const fgColorString = bgTinyColor.isLight() ? '#000' : '#fff';
      const bgColorString = bgTinyColor.toRgbString();
      const style = {backgroundColor: bgColorString, color: fgColorString};
      authorId = <li className="authorId">
        ID:{nbsp}
        <span className="authorIdSlug" style={style}>
          {this.props.post.anonymized_author_identifier}
        </span>
      </li>;
    }
    // TODO(amstocker): prob a better way to toggle focused css props?
    //                  I'm not sure of the best way to do this...
    return <div className={classNames({'post': true, 'focused': this.props.focused})} onClick={this.handleClick}>
      <div className="post-inner">
        <div className="title">
          <ul>
            <li className="author">
              Anonymous
            </li>
            <li className="timestamp" title={relativeTimestamp}>
              {absoluteTimestamp}
            </li>
            {authorId}
          </ul>
        </div>
        <div className="content">
          {this.props.post.content}
        </div>
      </div>
    </div>
  }
}

const Post = connect(
  (state, ownProps) => {
    return {
      focused: ownProps.post.id === state.get('focused')
    }
  },
  dispatch => {
    return {
      focusPost: id => {
        dispatch(focusPost(id));
      }
    };
  }
)(PostComponent);

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
        parent_id: this.props.focused_post_id,
        content: this.state.content
      });
      this.setState({content: ''});
    }
  }

  render() {
    const button_text = "Add Post" + (this.props.focused_post_id
        ? " (replying to post_id = " + this.props.focused_post_id + ")"
        : ""
    );
    return <div className="add-post">
      <div className="textarea">
        <textarea value={this.state.content} onChange={this.handleTextareaChange.bind(this)} />
      </div>
      <div className="controls">
        <button onClick={this.submitButtonClicked.bind(this)}>{button_text}</button>
      </div>
    </div>;
  }
}

const AddPost = connect(
  state => {
    return {
      focused_post_id: state.get('focused')
    };
  },
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

class PostTreeComponent extends Component {
  render() {
    const root = this.props.root;
    const children = root.children
                            .toArray()
                            .sort((x, y) => x.value.created - y.value.created);
    return <div className="post-node">
      {(root.id >= 0) && <Post post={root.value} />}
      {children.map(child =>
        <PostTreeComponent key={child.value.id} root={child} /> 
      )}
    </div>;
  }
}

const PostTree = connect(
  state => {
    return {root: state.get('post_graph').rootNode}
  }
)(PostTreeComponent);

class HomeComponent extends Component {
  render() {
    return <div>
      This is the index page.<br />
      <Link to="/about">About page</Link><br />
      <div>
        <PostTree />
        <AddPost />
      </div>
    </div>;
  }
}

const Home = connect()(HomeComponent);

export default Home;
