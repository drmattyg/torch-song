import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';
import Slider from 'material-ui/Slider';
import IconButton from 'material-ui/IconButton';
import FontIcon from 'material-ui/FontIcon';
import {Label, SimpleToggle} from './Widgets.jsx'

import {ColorWheel} from './Common.jsx'

export class SongbookPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.isPaused = false
    this.post = this.post.bind(this);
    this.sendCalibrate = this.sendCalibrate.bind(this);
    this.sendRewind = this.sendRewind.bind(this);
    this.sendStop = this.sendStop.bind(this);
    this.sendPlay= this.sendPlay.bind(this);
    this.sendFastForward = this.sendFastForward.bind(this);

    setInterval(() => {
      if (window.torchData) {
        this.setState({currentSong: window.torchData.current_song})
      }
    }, 250)

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
      console.log('Error sending JSON command')
    }).then((res) => {
      if (res.status == 200) {
        console.log('sent command')
      }
    });
  }

  sendCalibrate() { this.post({calibrate: true})}
  sendRewind() { this.post({rewind: true})}
  sendStop() { this.post({stop: true})}
  sendPlay() { this.post({play: true})}
  sendFastForward() { this.post({fastForward: true})}

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='control-page'>
        <Paper style={{padding:'20px'}}>
          <RaisedButton
            label="CALIBRATE"
            icon={<FontIcon className="material-icons">compare_arrows</FontIcon>}
            onTouchTap={this.sendCalibrate}
          />
          <IconButton iconClassName="material-icons" onTouchTap={this.sendRewind}>fast_rewind</IconButton>
          <IconButton iconClassName="material-icons" onTouchTap={this.sendStop}>stop</IconButton>
          <IconButton iconClassName="material-icons" onTouchTap={this.sendPlay}>play_arrow</IconButton>
          <IconButton iconClassName="material-icons" onTouchTap={this.sendFastForward}>fast_forward</IconButton>
          <Label label="Now Playing" value={this.state.currentSong}/>
        </Paper>
      </div>
    );
  }
};

