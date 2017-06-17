import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';

export class YAMLPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      json: {loading: 'loading'},
      shouldAlert: false,
      message: ''
    };
    var that = this
    this.restoreDefault = this.restoreDefault.bind(this);
    this.fetch = this.fetch.bind(this);
    this.post = this.post.bind(this);
    this.fetch(true);
  }

  post() {
    fetch('/default-mod-yaml', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.state.json)
    }).catch(() => {
      this.setState({shouldAlert: true, message: 'Error saving YAML file'})
    }).then((res) => {
      if (res.status == 200) {
        this.setState({shouldAlert: true, message: 'Saved YAML file'})
      } else {
        this.setState({shouldAlert: true, message: 'Error saving YAML file'})
      }
    });
  }

  fetch(silent) {
    fetch('/default-mod-yaml').then((resp) => {
      return resp.json()
    }).then((json) => {
      this.setState({json: json, shouldAlert: !silent, message: 'Loaded YAML file'})
    });
  }

  restoreDefault() {
    fetch('/default-yaml').then((resp) => {
      return resp.json()
    }).then((json) => {
      this.setState({json: json}, function() {
        this.post()
      })
    });
  }

  notify() {

  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='yaml-page'>
        <Snackbar open={this.state.shouldAlert} autoHideDuration={1000}
            onRequestClose={() => { this.setState({shouldAlert: false}) }}
            message={this.state.message} />

        <Paper style={{padding:'20px'}}>
          <div className='yaml-button-row'>
            <RaisedButton label="Restore " style={style} onTouchTap={this.restoreDefault}/>
            <RaisedButton label="Load" style={style} onTouchTap={this.fetch}/>
            <RaisedButton label="Submit" style={style} onTouchTap={this.post}/>
          </div>
          <hr />
          <ObjectTreeEditor key={-1} tree={this.state.json} level={0} notify={this.notify.bind(this)}/>
          <hr />
          <div className='yaml-button-row'>
            <RaisedButton label="Restore " style={style} onTouchTap={this.restoreDefault}/>
            <RaisedButton label="Load" style={style} onTouchTap={this.fetch}/>
            <RaisedButton label="Submit" style={style} onTouchTap={this.post}/>
          </div>
        </Paper>
      </div>
    );
  }
};

const pad = function(spaces) {
  let str = '';
  while (spaces) {
    str = str + '• ';
    spaces = spaces - 1;
  };
  return str;
};

class KeyStringEditor extends React.Component {
  constructor(props) {
    super(props)
    this.state = {val: this.props.parent[this.props.k]};
    this.handleChange = this.handleChange.bind(this);
  }
  handleChange(event) {
    if (isNaN(event.target.value)) {
      this.props.parent[this.props.k] = event.target.value
    } else {
      this.props.parent[this.props.k] = Number(event.target.value)
    }
    this.setState({val: event.target.value})
    this.props.notify()
  }
  render () {
    return (
      <div className='yaml-form-wrapper'>
        <label className='yaml-form-label'>
          <span className='yaml-form-dots'>{pad(this.props.level)}</span>{this.props.k}:
        </label>
        <input className='yaml-form-input' type='text' value={this.state.val} onChange={this.handleChange} />
      </div>
    )
  }
};

let uniqueId = 1;

export class ObjectTreeEditor extends React.Component {
  constructor(props) {
    super(props)
    this.nextLevel = this.props.level + 1
  }

  renderObjects(objs) {
    return Object.keys(objs).map(function (key) {
      uniqueId = uniqueId + 1;
      const type = typeof(objs[key])
      if (type == 'object') {
        return (
          <div key={uniqueId}>
            <label className='yaml-tree-label'>
              <span className='yaml-form-dots'>{pad(this.props.level)}</span>{key}
            </label>
            <ObjectTreeEditor tree={objs[key]} level={this.nextLevel} notify={this.props.notify}/>
          </div>
        )
      } else {
        return <KeyStringEditor key={uniqueId} level={this.props.level} k={key} parent={objs} notify={this.props.notify}/>
      }
    }, this);
  }

  render() {
    return (
      <div>
        { this.renderObjects(this.props.tree) }
      </div>
    )
  }
};
