import React, {Component} from 'react';
import {connect} from 'react-redux';
import moment from 'moment';
import tinycolor from 'tinycolor2';
import classNames from 'classnames';

import * as actions from 'actions';
import {pickColorFromString, nbsp} from 'Utils';


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
    const relativeTimestamp = created.from(this.props.now);
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
            <li>
            {this.props.post.score ? (this.props.post.score).toFixed(4) : "N/A"}
            </li>
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
      focused: ownProps.post.id === state.get('focused'),
      now: state.get('timestamp'),
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

export default Post;
