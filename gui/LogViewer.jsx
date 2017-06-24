import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';

import {ColorWheel} from './Common.jsx'

export class LogPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      shouldAlert: false,
      message: ''
    };
    this.fetch = this.fetch.bind(this);
    this.fetch(false);
    this.clear = this.clear.bind(this);

    setInterval(() => {
      this.fetch(true)
    }, 100)
  }

  clear() {
    fetch('/logs_clear', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    }).catch(() => {
      this.setState({shouldAlert: true, message: 'Error clearing logs'})
    }).then((res) => {
      if (res.status == 200) {
        this.setState({shouldAlert: true, message: 'Cleared logs'})
      } else {
        this.setState({shouldAlert: true, message: 'Error clearing logs'})
      }
    });
  }


  fetch(silent) {
    fetch('/logs').then((resp) => {
      return resp.json()
    }).then((json) => {
      this.setState({data: json, shouldAlert: !silent, message: 'Loaded logs'})
    });
  }

  renderLogRecords(data) {
    return data.map((record, i) => {
      return (
        <LogRecord key={i} record={record} />
      )
    });
  }

  render() {
    const style = {
      margin: 10
    };
    return (
      <div className='log-page'>
        <Snackbar open={this.state.shouldAlert} autoHideDuration={1000}
            onRequestClose={() => { this.setState({shouldAlert: false}) }}
            message={this.state.message} />
        <Paper style={{padding:'20px'}}>
          <div className='log-button-row'>
            <RaisedButton label="Clear" style={style} onTouchTap={this.clear}/>
          </div>
          <hr />
            <div className="logs">
              { this.renderLogRecords(this.state.data) }
            </div>
          <hr />
          <div className='log-button-row'>
            <RaisedButton label="Clear" style={style} onTouchTap={this.clear}/>
          </div>
        </Paper>
      </div>
    );
  }
};

class LogRecord extends React.Component {
  constructor(props) {
    super(props)
  }

  formatDate(date) {
    return date.getMonth()+1 + '/' + date.getDate() + '/' + date.getFullYear() +
      ' ' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() +
      '.' + date.getMilliseconds()
  }

  render() {
    const r = this.props.record
    const edge_id = r.edge_id || 1
    const date = this.formatDate(new Date(r.time * 1000));
    const timeColor = r.levelno == 40 ? 'red' : 'black'
    const textColor = r.levelno == 40 ? 'red' : ColorWheel[edge_id]
    return (
      <div className='log-record'>
        <span className='log-time' style={{color: timeColor}}> [{date + ' ' +  r.levelname}]</span>
        <span className='log-message' style={{color: textColor}}>  {r.message} </span>
      </div>
    )
  }
};
