import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';
import Slider from 'material-ui/Slider';
import IconButton from 'material-ui/IconButton';
import FontIcon from 'material-ui/FontIcon';
import LinearProgress from 'material-ui/LinearProgress'
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
    this.sendRun = this.sendRun.bind(this);
    this.sendStop= this.sendStop.bind(this);
    this.sendEstop= this.sendEstop.bind(this);

    setInterval(() => {
      if (window.torchData) {
        this.setState({currentSong: window.torchData.current_song,
                       nextSong: window.torchData.next_song,
                       currentSongTime: window.torchData.current_song_time,
                       endSongTime: window.torchData.end_song_time})
      }
    }, 250)

  }

  formatSongTime(time) {
    let minutes = Math.floor(time / 1000 / 60).toFixed(0);
    if (minutes < 10) minutes = '0' + minutes;
    let seconds = Math.floor(time / 1000).toFixed(0);
    if (seconds < 10) seconds = '0' + seconds;
    return minutes + ':' + seconds
  }

  post(url, command) {
    fetch('/' + url, {
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

  sendCalibrate() { this.post('control', {calibrate: true})}
  sendRewind() { this.post('control', {prev: true})}
  sendStop() { this.post('control', {stop: true})}
  sendPlay() { this.post('control', {play: true})}
  sendFastForward() { this.post('control', {next: true})}
  sendRun() { this.post('proc', {proc: 'start'})}
  sendStop() { this.post('proc', {proc: 'stop'})}
  sendEstop() { this.post('proc', {proc: 'estop'})}

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='control-page'>
        <Paper style={{padding:'10px'}}>
          <h2>Torchsong</h2>
          <div className="song-process">
            <RaisedButton
              className="song-process-button"
              label="RUN"
              icon={<FontIcon className="material-icons">directions_run</FontIcon>}
              onTouchTap={this.sendRun}
            />
            <RaisedButton
              className="song-process-button"
              label="STOP"
              icon={<FontIcon className="material-icons">accessibility</FontIcon>}
              onTouchTap={this.sendStop}
            />
            <RaisedButton
              className="song-process-button"
              label="CAL"
              icon={<FontIcon className="material-icons">compare_arrows</FontIcon>}
              onTouchTap={this.sendCalibrate}
            />
            <RaisedButton
              className="song-process-button"
              label="KILL"
              icon={<FontIcon className="material-icons">error</FontIcon>}
              onTouchTap={this.sendEstop}
            />
          </div>
          <h2>Songbook Control</h2>
          <div className="song-controls-outter">
            <div className="song-controls-inner">
              <div className="song-control">
                <IconButton iconClassName="material-icons" onTouchTap={this.sendRewind}>fast_rewind</IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons" onTouchTap={this.sendStop}>stop</IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons" onTouchTap={this.sendPlay}>play_arrow</IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons" onTouchTap={this.sendFastForward}>fast_forward</IconButton>
              </div>
            </div>
          </div>
          <Label className='song-current' label="Now Playing" value={this.state.currentSong}/>
          <Label className='song-next' label="Next Up" value={this.state.nextSong}/>
          <div>
            <div className='song-time'>{this.formatSongTime(this.state.currentSongTime)}</div>
            <div className='song-time-bar'>
              <LinearProgress max={this.state.endSongTime} value={this.state.currentSongTime}
              mode={'determinate'}/>
            </div>
            <div className='song-time'>{this.formatSongTime(this.state.endSongTime)}</div>
          </div>
        </Paper>
      </div>
    );
  }
};

