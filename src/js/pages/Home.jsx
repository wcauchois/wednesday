import React, {Component} from 'react';
import {connect} from 'react-redux';
import ReactDOM from 'react-dom';
import {Shortcuts} from 'react-shortcuts';
import {WindowResizeListener} from 'react-window-resize-listener';

import * as actions from 'actions';
import {withoutScrolling} from 'Utils';
import Transport from 'Transport';

import PostTree from 'components/PostTree';
import PostPreviewList from 'components/PostPreviewList';
import AddPost from 'components/AddPost';


class HomeComponent extends Component {
  constructor(props) {
    super(props);
  }

  _handleShortcuts(action, event) {
    if (action === 'MOVE_UP') {
      this.props.moveFocus(1);
    } else if (action === 'MOVE_DOWN') {
      this.props.moveFocus(-1);
    } else if (action === 'FOCUS_INPUT') {
      if (this.addPostRef) {
        event.preventDefault();
        ReactDOM.findDOMNode(this.addPostRef).querySelector('textarea').focus();
      }
    }
  }

  onAddPostTextareaEscape() {
    if (this.shortcutsRef) {
      withoutScrolling(() => {
        ReactDOM.findDOMNode(this.shortcutsRef).focus();
      });
    }
  }

  onWindowResize() {
    if (this.postPreviewListRef) {
      const offsetWidth = ReactDOM.findDOMNode(this.postPreviewListRef).offsetWidth;
      this.props.setAddPostMarginLeft(offsetWidth);
    }
  }

  render() {
    return (
      <div className="grid-container">
        <WindowResizeListener onResize={this.onWindowResize.bind(this)} />
        <PostPreviewList
          ref={(postPreviewList) => { this.postPreviewListRef = postPreviewList; }} />
        <div className="post-view">
          <span className="grid-column-header">{"CHAT"}</span>
          <Shortcuts
            name='HOME'
            handler={this._handleShortcuts.bind(this)}
            ref={(shortcuts) => { this.shortcutsRef = shortcuts; }}>
            <div>
              {this.props.roots.map((root, id) =>
                <PostTree key={id} root={root} />
              )}
            </div>
          </Shortcuts>
          <AddPost
            onTextareaEscape={this.onAddPostTextareaEscape.bind(this)}
            ref={(addPost) => { this.addPostRef = addPost; }} />
        </div>
      </div>
    );
  }

  componentDidMount() {
    // NOTE(amstocker): this is just a temporary way to show all posts
    Transport.call.getTopLevels().then(res => {
      for (const post of res) {
        Transport.call.subscribe({id: post.id});
        Transport.call.getTree({id: post.id}).then(res => {
          store.dispatch(actions.addTree(res));
        });
      }
    });

    // start polling for hot posts
    store.dispatch(actions.hotPostsPoll(1000));

    // This is a tiny bit hacky
    ReactDOM.findDOMNode(this).querySelector('shortcuts').focus();
  }
}

const Home = connect(
  state => {
    return {
      roots: state.get('post_store').roots,
    };
  },
  dispatch => {
    return {
      moveFocus: delta => dispatch(actions.moveFocus(delta)),
      setAddPostMarginLeft: value => dispatch(actions.setAddPostMarginLeft(value)),
    };
  }
)(HomeComponent);

export default Home;
