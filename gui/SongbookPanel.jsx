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

export class SongbookPanel extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.isPaused = false
    this.post = this.post.bind(this);
    this.sendCalibrate = this.sendCalibrate.bind(this);
    this.sendRewind = this.sendRewind.bind(this);
    this.sendPlayStop = this.sendPlayStop.bind(this);
    this.sendPlay= this.sendPlay.bind(this);
    this.sendFastForward = this.sendFastForward.bind(this);

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
      this.props.notify('Error sending JSON command')
    }).then((res) => {
      if (res.status == 200) {
      }
    });
  }

  sendCalibrate() {
    this.post('control', {calibrate: true})
    this.props.notify('Calibrating')
  }
  sendRewind() { this.post('control', {prev: true})}
  sendPlayStop() { this.post('control', {stop: true})}
  sendPlay() { this.post('control', {play: true})}
  sendFastForward() { this.post('control', {next: true})}

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
              onTouchTap={this.props.run}
            />
            <RaisedButton
              className="song-process-button"
              label="STOP"
              icon={<FontIcon className="material-icons">accessibility</FontIcon>}
              onTouchTap={this.props.stop}
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
              onTouchTap={this.props.estop}
            />
          </div>
          <h2>Songbook Control</h2>
          <div className="song-controls-outter">
            <div className="song-controls-inner">
              <div className="song-control">
                <IconButton iconClassName="material-icons"
                  onTouchTap={this.sendRewind}
                  hoveredStyle={{backgroundColor: '#eee'}}>
                  fast_rewind
                </IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons"
                  onTouchTap={this.sendPlayStop}
                  hoveredStyle={{backgroundColor: '#eee'}}>
                  stop
                </IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons"
                  onTouchTap={this.sendPlay}
                  hoveredStyle={{backgroundColor: '#eee'}}>
                  play_arrow
                </IconButton>
              </div>
              <div className="song-control">
                <IconButton iconClassName="material-icons"
                  onTouchTap={this.sendFastForward}
                  hoveredStyle={{backgroundColor: '#eee'}}>
                  fast_forward
                </IconButton>
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

