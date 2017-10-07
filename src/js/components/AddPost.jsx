import React, {Component} from 'react';
import {connect} from 'react-redux';

import * as actions from 'actions';


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
    if (event.keyCode === 13 && !event.shiftKey) { // Enter
      event.preventDefault();
      this.submitButtonClicked();
    } else if (event.keyCode === 27) { // Escape
      if (this.props.onTextareaEscape) {
        this.props.onTextareaEscape();
      }
    }
  }

  render() {
    let button_text;
    if (this.props.focused_post_id) {
      button_text = `Add Post (replying to post_id = ${this.props.focused_post_id})`;
    } else {
      button_text = `Select a post to reply`;
    }
    return <div className="add-post">
      <div className="add-post-inner">
        <textarea value={this.state.content} onChange={this.handleTextareaChange.bind(this)}
          onKeyDown={this.handleTextareaKeyDown.bind(this)}
          placeholder="Write something..." />
        <div className="controls">
          <button onClick={this.submitButtonClicked.bind(this)}
            disabled={!this.props.focused_post_id}>{button_text}</button>
        </div>
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

export default AddPost;
