import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';
import Slider from 'material-ui/Slider';
import {SimpleToggle} from './Widgets.jsx'

import {ColorWheel} from './Common.jsx'

export class SongbookPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
    this.isPaused = false
    this.post = this.post.bind(this);
    this.sendPause = this.sendPause.bind(this, 1)
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

  sendPause() {
    this.isPaused = !this.isPaused
    this.post({pause: this.isPaused})
  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='control-page'>
        <Paper style={{padding:'20px'}}>
          <RaisedButton label='||' onTouchTap={this.sendPause}/>
        </Paper>
      </div>
    );
  }
};

