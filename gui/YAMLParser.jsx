import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';

export class YAMLPanel extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      json: {loading: 'loading'},
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
      this.props.notify('Error saving YAML file')
    }).then((res) => {
      if (res.status == 200) {
        this.props.notify('Saved YAML file')
      } else {
        this.props.notify('Error saving YAML file')
      }
    });
  }

  fetch(silent) {
    fetch('/default-mod-yaml').then((resp) => {
      return resp.json()
    }).catch(() => {
      this.props.notify('Error loading YAML file: default-mod.yml')
    }).then((json) => {
      this.setState({json: json})
      this.props.notify('Loaded YAML file')
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
        <Paper style={{padding:'20px'}}>
          <div className='yaml-button-row'>
            <RaisedButton label="Default" style={style} onTouchTap={this.restoreDefault}/>
            <RaisedButton label="Reload" style={style} onTouchTap={this.fetch}/>
            <RaisedButton label="Save" style={style} onTouchTap={this.post}/>
          </div>
          <hr />
          <ObjectTreeEditor key={-1} tree={this.state.json} level={0} notify={this.notify.bind(this)}/>
          <hr />
          <div className='yaml-button-row'>
            <RaisedButton label="Default" style={style} onTouchTap={this.restoreDefault}/>
            <RaisedButton label="Reload" style={style} onTouchTap={this.fetch}/>
            <RaisedButton label="Save" style={style} onTouchTap={this.post}/>
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

class KeyStringEditor extends React.PureComponent {
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

export class ObjectTreeEditor extends React.PureComponent {
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
