import React from 'react';
import {render} from 'react-dom';

import 'whatwg-fetch';

import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';

import {ColorWheel} from './Common.jsx'

export class LogPanel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      logs: []
    };
    this.clear = this.clear.bind(this);

    var that = this
    setInterval(() => {
      if (window.logs) {
        this.setState({logs: window.logs})
      }
    }, 250)
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
      this.props.notify('Error clearing logs')
    }).then((res) => {
      if (res.status == 200) {
        this.props.notify('Cleared logs')
      } else {
        this.props.notify('Error clearing logs')
      }
    });
  }


  renderLogRecords(data, errorsOnly) {
    return data.filter((el) => {
      return errorsOnly ? el.levelno == 40 : true
    }).map((record, i) => {
      return (
        <LogRecord key={i} record={record} />
      )
    });
  }

  render() {
    const style = {
      margin: 10
    };
    const showControls = this.props.showControls ? 'block' : 'none'
    return (
      <div className='log-page'>
        <Paper style={{padding:'20px'}}>
          <div className='log-button-row' style={{display:showControls}}>
            <RaisedButton label="Clear" style={style} onTouchTap={this.clear}/>
          </div>
          <hr />
            <div className="logs">
              { this.renderLogRecords(this.state.logs, this.props.errorsOnly) }
            </div>
          <hr />
          <div className='log-button-row' style={{display:showControls}}>
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
    const edge_id = r.edge_id || 0
    const date = this.formatDate(new Date(r.time * 1000));
    const timeColor = r.levelno == 40 ? 'red' : 'black'
    const textColor = r.levelno == 40 ? 'red' : ColorWheel[edge_id]
    return (
      <div className='log-record'>
        <span className='log-time' style={{color: timeColor}}> [{date}]{r.levelname}</span>
        <span className='log-message' style={{color: textColor}}>  {r.message} </span>
      </div>
    )
  }
};
