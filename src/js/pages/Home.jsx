import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Link} from 'react-router-dom';
import moment from 'moment';
import tinycolor from 'tinycolor2';
import classNames from 'classnames';

import * as actions from 'actions';
import {pickColorFromString, nbsp} from 'Utils';
import Transport from 'Transport';


class PostComponent extends Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.focusPost(this.props.post.id);
  }

  authorIdentifierStyle() {
    const identifier = this.props.post.anonymized_author_identifier;
    if (identifier) {
      const bgColor = pickColorFromString(identifier);
      const bgTinyColor = tinycolor({r: bgColor[0], g: bgColor[1], b: bgColor[2]});
      const fgColorString = bgTinyColor.isLight() ? '#000' : '#fff';
      const bgColorString = bgTinyColor.toRgbString();
      return {
        backgroundColor: bgColorString,
        color: fgColorString
      };
    } else {
      return {};
    }
  }

  render() {
    const created = moment.min(moment.unix(this.props.post.created), moment.utc());
    const absoluteTimestamp = created.format('MMMM Do YYYY, h:mm:ss a');
    const relativeTimestamp = created.fromNow();
    let authorId;
    if (this.props.post.anonymized_author_identifier) {
      authorId = <li className="authorId">
        ID:{nbsp}
        <span className="authorIdSlug" style={this.authorIdentifierStyle()}>
          {this.props.post.anonymized_author_identifier}
        </span>
      </li>;
    }
    return <div className={classNames({'post': true, 'focused': this.props.focused})} onClick={this.handleClick}>
      <div className="post-inner">
        <div className="title">
          <ul>
            <li className="author">
              Anonymous
            </li>
            <li className="timestamp" title={absoluteTimestamp}>
              {relativeTimestamp}
            </li>
            {authorId}
          </ul>
        </div>
        <div className="content">
          {this.props.post.content}
        </div>
      </div>
      {this.props.focused && <AddPost />}
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
        dispatch(actions.focusPost(id));
      }
    };
  }
)(PostComponent);


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
      this.props.newPost({
        parent_id: this.props.focused_post_id,
        content: this.state.content
      });
      this.setState({content: ''});
    }
  }

  handleTextareaKeyDown(event) {
    // Cmd+enter
    if (event.keyCode === 13 && event.metaKey) {
      this.submitButtonClicked();
    }
  }

  render() {
    const button_text = "Add Post (replying to post_id = " + this.props.focused_post_id + ")";
    return <div className="add-post">
      <div className="textarea">
        <textarea value={this.state.content} onChange={this.handleTextareaChange.bind(this)}
          onKeyDown={this.handleTextareaKeyDown.bind(this)} />
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
      newPost: (post_values) => dispatch(actions.newPost(post_values))
    };
  }
)(AddPostComponent);


class HomeComponent extends Component {
  render() {
    return <div>
      This is the index page.<br />
      <Link to="/about">About page</Link><br />
      <div>
        {this.props.roots.map((root, id) =>
          <PostTree key={id} root={root} />
        )} 
      </div>
    </div>;
  }

  // NOTE(amstocker): this is just a temporary way to show all posts
  componentDidMount() {
    Transport.call.get_toplevels().then(res => {
      for (const post of res) {
        Transport.call.subscribe({id: post.id});
        Transport.call.get_tree({id: post.id}).then(res => {
          store.dispatch(actions.addTree(res));
        });
      }
    });
  }
}

const Home = connect(
  state => {
    return {roots: state.get('post_store').roots}
  }
)(HomeComponent);

export default Home;
