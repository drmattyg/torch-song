import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';
import Slider from 'material-ui/Slider';
import FontIcon from 'material-ui/FontIcon';
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

  renderEdgeControls() {
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return arr.map((i) => {
      return (
        <EdgeControl key={i} edge_id={i} post={this.post}/>
      )
    });
  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='control-page'>
        <Paper style={{padding:'20px'}}>
          { this.renderEdgeControls() }
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
    this.state = {
      pos: 0
    };

    var that = this
    setInterval(() => {
      if (window.torchData[that.props.edge_id]) {
        const d = window.torchData[that.props.edge_id];
        this.setState({pos: d['position'], igniter: d['igniter'], valve: d['valve']})
      }
    }, 100)
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
    const edgeColor = ColorWheel[this.props.edge_id];
    const igniterColor = this.state.igniter ? edgeColor : 'black'
    const valveColor = this.state.valve ? edgeColor : 'black'
    return (
      <div className='edge-control' >
        <h2 style={{backgroundColor: edgeColor}}>Edge {this.props.edge_id}</h2>
        <div className='edge-control-items'>
          <div className='edge-icons'>
            <FontIcon className="material-icons" color={igniterColor}>smoking_rooms</FontIcon>
            <FontIcon className="material-icons" color={valveColor}>brightness_high</FontIcon>
          </div>
          <Slider value={this.state.pos} disabled={true} min={0} max={1} />
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

