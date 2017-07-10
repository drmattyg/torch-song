import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';
import RaisedButton from 'material-ui/RaisedButton';

export class TorchsongPanel extends React.PureComponent {
  constructor(props) {
    super(props);
    this.post = this.post.bind(this);
    this.start = this.start.bind(this)
    this.stop = this.stop.bind(this)
    this.restart = this.restart.bind(this)
  }

  post(json) {
    fetch('/proc', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(json)
    }).catch(() => {
      console.log('Error sending')
    }).then((res) => {
      if (res.status == 200) {
      } else {
        console.log('Error sending')
      }
    });
  }

  start() {
    this.post({proc: 'start'});
  }

  stop() {
    this.post({proc: 'stop'});
  }

  restart() {
    this.stop()
    this.start()
  }

  render() {
    return (
      <div className='torchsong-page'>
        <RaisedButton label="Start" onTouchTap={this.start}/>
        <RaisedButton label="Stop" onTouchTap={this.stop}/>
        <RaisedButton label="Restart" onTouchTap={this.restart}/>
      </div>
    )
  }
}
