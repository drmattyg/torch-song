import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';
import {SimpleToggle} from './Widgets.jsx'

import {ColorWheel} from './Common.jsx'

export class ControlPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      json: {loading: 'loading'},
      shouldAlert: false,
      message: ''
    };
    this.post = this.post.bind(this);
  }

  post(command) {
    fetch('/control', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(command)
    }).catch(() => {
      this.setState({shouldAlert: true, message: 'Error sending command'})
    }).then((res) => {
      if (res.status == 200) {
        console.log('sent command')
      } else {
        this.setState({shouldAlert: true, message: 'Error sending command'})
      }
    });
  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='control-page'>
        <Snackbar open={this.state.shouldAlert} autoHideDuration={1000}
            onRequestClose={() => { this.setState({shouldAlert: false}) }}
            message={this.state.message} />
        <Paper style={{padding:'20px'}}>
          <EdgeControl edge_id={1} post={this.post}/>
          <EdgeControl edge_id={2} post={this.post}/>
          <EdgeControl edge_id={3} post={this.post}/>
          <EdgeControl edge_id={4} post={this.post}/>
          <EdgeControl edge_id={5} post={this.post}/>
          <EdgeControl edge_id={6} post={this.post}/>
          <EdgeControl edge_id={7} post={this.post}/>
          <EdgeControl edge_id={8} post={this.post}/>
          <EdgeControl edge_id={9} post={this.post}/>
        </Paper>
      </div>
    );
  }
};

export class EdgeControl extends React.Component {
  constructor(props) {
    super(props)
    this.sendOverride = this.sendOverride.bind(this)
    this.sendIgniter = this.sendIgniter.bind(this)
    this.sendValve = this.sendValve.bind(this)
    this.jogFwd = this.jog.bind(this, 1)
    this.jogRev = this.jog.bind(this, -1)
  }

  sendIgniter(e, s) {
    const id = this.props.edge_id
    this.props.post({id: id, igniter: s})
  }
  sendValve(e, s) {
    const id = this.props.edge_id
    this.props.post({id: id, valve: s})
  }
  sendOverride(e, s) {
    const id = this.props.edge_id
    this.props.post({id: id, override: s})
  }
  jog(dir, e) {
    const id = this.props.edge_id
    this.props.post({id: id, dir: dir, speed: 80})
    let timer = setTimeout(() => {
      this.props.post({id: id, dir: dir, speed: 0})
      clearTimeout(timer)
    }, 500);
  }

  render () {
    return (
      <div className='edge-control' >
        <h2 style={{backgroundColor: ColorWheel[this.props.edge_id]}}>Edge {this.props.edge_id}</h2>
        <div className='edge-control-items'>
          <SimpleToggle label='Override' onToggle={this.sendOverride} />
          <SimpleToggle label='Igniter' onToggle={this.sendIgniter} />
          <SimpleToggle label='Valve' onToggle={this.sendValve} />
          <RaisedButton label='<<' onTouchTap={this.jogRev} />
          <RaisedButton label='>>' onTouchTap={this.jogFwd} />
        </div>
      </div>
    )
  }
};

