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

export class ControlPanel extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      json: {loading: 'loading'},
      overridesDisabled: false
    };
    this.post = this.post.bind(this);
    this.masterOverride = this.masterOverride.bind(this)
    this.showFold = this.showFold.bind(this)
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
      this.props.notify('Error sending command')
    }).then((res) => {
      if (res.status == 200) {
      } else {
        this.props.notify('Error sending command')
      }
    });
  }

  masterOverride(e, s) {
    for (let i = 1; i <= 9; i += 1) {
      this.post({id: i, override: s})
    }
    this.setState({overridesDisabled: s});
  }

  showFold(e, s) {
    this.setState({showFold: s})
  }

  renderEdgeControls() {
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return arr.map((i) => {
      return (
        <EdgeControl key={i} edge_id={i} post={this.post}
          overridesDisabled={this.state.overridesDisabled}
          showFold={this.state.showFold}
        />
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
          <div className='master-controls'>
            <div className='master-control'>
              <SimpleToggle label='Show Overrides' onToggle={this.showFold} />
            </div>
            <div className='master-control'>
              <SimpleToggle label='Master Override' onToggle={this.masterOverride} />
            </div>
          </div>
          { this.renderEdgeControls() }
        </Paper>
      </div>
    );
  }
};

export class EdgeControl extends React.PureComponent {
  constructor(props) {
    super(props)
    this.sendOverride = this.sendOverride.bind(this)
    this.sendIgniter = this.sendIgniter.bind(this)
    this.sendValve = this.sendValve.bind(this)
    this.sendCalibrate = this.sendCalibrate.bind(this)
    this.sendStop = this.sendStop.bind(this)
    this.jogFwd = this.jog.bind(this, 1)
    this.jogRev = this.jog.bind(this, -1)
    this.rev = this.rev.bind(this)
    this.fwd = this.fwd.bind(this)
    this.state = {
      pos: 0
    };

    var that = this
    setInterval(() => {
      if (window.torchData[that.props.edge_id]) {
        const d = window.torchData[that.props.edge_id];
        this.setState({
          pos: d['position'],
          igniter: d['igniter'],
          valve: d['valve'],
          revLimit: d['rev_limit'],
          fwdLimit: d['fwd_limit'],
        })
      }
    }, 100)
  }

  sendIgniter(e, s) {
    const id = this.props.edge_id
    this.props.post({id: id, igniter: s})
  }
  sendCalibrate(e) {
    const id = this.props.edge_id
    this.props.post({id: id, calibrate_single: true})
  }
  sendStop(e) {
    const id = this.props.edge_id
    this.props.post({id: id, dir: 0, speed: 0})
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
  rev(e) {
    const id = this.props.edge_id
    this.props.post({id: id, dir: -1, speed: 80})
  }
  fwd(e) {
    const id = this.props.edge_id
    this.props.post({id: id, dir: 1, speed: 80})
  }

  render () {
    const edgeColor = ColorWheel[this.props.edge_id];
    const igniterColor = this.state.igniter ? edgeColor : 'black'
    const valveColor = this.state.valve ? edgeColor : 'black'
    const revLimit = this.state.revLimit ? edgeColor : 'black'
    const fwdLimit = this.state.fwdLimit ? edgeColor : 'black'
    return (
      <div className='edge-control' >
        <h2 style={{backgroundColor: edgeColor}}>Edge {this.props.edge_id}</h2>
        <div className='edge-control-items'>
          <div className='edge-icons'>
            <FontIcon className="material-icons" color={revLimit}>chevron_left</FontIcon>
            <FontIcon className="material-icons" color={igniterColor}>smoking_rooms</FontIcon>
            <FontIcon className="material-icons" color={valveColor}>brightness_high</FontIcon>
            <FontIcon className="material-icons" color={fwdLimit}>chevron_right</FontIcon>
          </div>
          <Slider value={this.state.pos} disabled={true} min={0} max={1} />
          <div className={this.props.showFold ? '' : 'hidden'} >
            <SimpleToggle label='Override' onToggle={this.sendOverride}
                disabled={this.props.overridesDisabled}/>
            <div className='edge-buttons'>
              <div className='edge-toggle'>
                <SimpleToggle label='Igniter' onToggle={this.sendIgniter} />
              </div>
              <div className='edge-toggle'>
                <SimpleToggle label='Valve' onToggle={this.sendValve} />
              </div>
            </div>
            <div className='edge-buttons'>
              <RaisedButton className='edge-motor-button' label='CAL'
                icon={<FontIcon className="material-icons">compare_arrows</FontIcon>}
                onTouchTap={this.sendCalibrate}
              />
              <RaisedButton className='edge-motor-button' label=''
                icon={<FontIcon className="material-icons">stop</FontIcon>}
                onTouchTap={this.sendStop}
              />
            </div>
            <div className='edge-buttons'>
              <RaisedButton className='edge-motor-button' label='<' onTouchTap={this.jogRev} />
              <RaisedButton className='edge-motor-button' label='>' onTouchTap={this.jogFwd} />
            </div>
            <div className='edge-buttons'>
              <RaisedButton className='edge-motor-button' label='<<' onTouchTap={this.rev} />
              <RaisedButton className='edge-motor-button' label='>>' onTouchTap={this.fwd} />
            </div>
          </div>
        </div>
      </div>
    )
  }
};

