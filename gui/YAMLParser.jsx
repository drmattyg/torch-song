import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import {ColorWheel} from './Common.jsx'

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
      this.props.notify('Error saving configuration')
    }).then((res) => {
      if (res.status == 200) {
        this.props.notify('Saved configuration')
      } else {
        this.props.notify('Error saving configuration')
      }
    });
  }

  fetch(silent) {
    fetch('/default-mod-yaml').then((resp) => {
      return resp.json()
    }).catch(() => {
      this.props.notify('Error loading configuration: default-mod.yml')
    }).then((json) => {
      this.setState({json: json})
      this.props.notify('Loaded configuration')
    });
  }

  restoreDefault() {
    fetch('/default-yaml').then((resp) => {
      return resp.json()
    }).then((json) => {
      this.props.notify('Loaded default configuration: default.yml')
      this.setState({json: json}, function() {
        this.post()
      })
    });
  }

  saveAndRestart() {
    this.post()
    this.props.restart()
  }

  enableEdge(id, e) {
    let json = this.state.json
    json['edges'].forEach((item, i) => {
      if (item.id == id) {
        let enabledState = json['edges'][i].enabled
        json['edges'][i].enabled = !enabledState
        this.setState({json: json})
        this.forceUpdate()
        this.saveAndRestart()
      }
    });
  }

  enableEdgeMotors(id, e) {
    let json = this.state.json
    json['edges'].forEach((item, i) => {
      if (item.id == id) {
        let enabledState = json['edges'][i].motors_enabled
        json['edges'][i].motors_enabled = !enabledState
        this.setState({json: json})
        this.forceUpdate()
        this.saveAndRestart()
      }
    });
  }

  renderEdgeDisables(json, style) {
    if (json['edges']) {
      return json.edges.map((item) => {
        let label = item.enabled ? 'Disable ' : 'Enable '
        label += item.id
        return (
          <RaisedButton labelColor={ColorWheel[item.id]} key={item.id} label={label}
              onTouchTap={this.enableEdge.bind(this, item.id)} style={style}/>
        )
      })
    } else {
      return
    }
  }

  renderEdgeDisableMotors(json, style) {
    if (json['edges']) {
      return json.edges.map((item) => {
        let label = item.motors_enabled ? 'Disable Motor' : 'Enable Motor '
        label += item.id
        return (
          <RaisedButton labelColor={ColorWheel[item.id]} key={item.id} label={label}
              onTouchTap={this.enableEdgeMotors.bind(this, item.id)} style={style}/>
        )
      })
    } else {
      return
    }
  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='yaml-page'>
        <Paper style={{padding:'20px'}}>
          <div className='yaml-button-row'>
            { this.renderEdgeDisables(this.state.json, style) }
          </div>
          <div className='yaml-button-row'>
            { this.renderEdgeDisableMotors(this.state.json, style) }
          </div>
          <div className='yaml-button-row'>
            <RaisedButton label="Default Config" style={style} onTouchTap={this.restoreDefault}/>
          </div>
          <hr />
          <ObjectTreeEditor key={-1} tree={this.state.json} level={0}
              cb={this.saveAndRestart.bind(this)}/>
          <hr />
          <div className='yaml-button-row'>
            { this.renderEdgeDisables(this.state.json, style) }
          </div>
          <div className='yaml-button-row'>
            { this.renderEdgeDisableMotors(this.state.json, style) }
          </div>
          <div className='yaml-button-row'>
            <RaisedButton label="Default Config" style={style} onTouchTap={this.restoreDefault}/>
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
    this.handleBlur = this.handleBlur.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.handleFocus = this.handleFocus.bind(this);
  }
  handleChange(event) {
    if (isNaN(event.target.value)) {
      const bool =
          event.target.value == 'true' ? true : (event.target.value == 'false' ? false : null)
      if (bool !== null) {
        this.props.parent[this.props.k] = bool
      } else {
        this.props.parent[this.props.k] = event.target.value
      }
    } else {
      this.props.parent[this.props.k] = Number(event.target.value)
    }
    this.setState({val: event.target.value})
  }
  handleBlur(e) {
    if (e.target.value != this.oldInput) {
      this.props.cb()
    }
  }
  handleFocus(e) {
    this.oldInput = e.target.value
  }
  handleKeyPress(e) {
    var code = (e.keyCode ? e.keyCode : e.which)
    if(code == 13) {
      this.props.cb()
    }
  }
  render () {
    return (
      <div className='yaml-form-wrapper'>
        <label className='yaml-form-label'>
          <span className='yaml-form-dots'>{pad(this.props.level)}</span>{this.props.k}:
        </label>
        <input className='yaml-form-input' type='text' value={this.state.val}
          onChange={this.handleChange} onBlur={this.handleBlur} onKeyPress={this.handleKeyPress}
          onFocus={this.handleFocus} />
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
            <ObjectTreeEditor tree={objs[key]} level={this.nextLevel} cb={this.props.cb}/>
          </div>
        )
      } else {
        return <KeyStringEditor key={uniqueId} level={this.props.level} k={key}
            parent={objs} cb={this.props.cb}/>
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
