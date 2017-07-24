import 'whatwg-fetch';

import React from 'react';
import {render} from 'react-dom';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';

import AppBar from 'material-ui/AppBar';
import {Tabs, Tab} from 'material-ui/Tabs';
import Snackbar from 'material-ui/Snackbar';

import {YAMLPanel} from './YAMLParser.jsx';
import {LogPanel} from './LogViewer.jsx';
import {ControlPanel} from './ControlPanel.jsx';
import {SongbookPanel} from './SongbookPanel.jsx';

// require to make Tabs work
const injectTapEventPlugin = require("react-tap-event-plugin");
injectTapEventPlugin();

const version = process.env.npm_package_version

class Components extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      logs: [],
      control: {},
      shouldAlert: false,
      message: '',
      connected: false
    };

    // We make data globally available to deal with some React limitations
    const arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    window.torchData = arr.map((i) => {
      return {
        position: 0,
        igniter: false,
        valve: false
      }
    })
    window.torchData.current_song = ''

    this.fetchLogs = this.fetchLogs.bind(this);
    this.fetchProc = this.fetchProc.bind(this);
    this.fetchTorchData = this.fetchTorchData.bind(this);
    this.notify = this.notify.bind(this);
    this.sendRun = this.sendRun.bind(this);
    this.sendStop = this.sendStop.bind(this);
    this.sendEstop = this.sendEstop.bind(this);
    this.sendRestart = this.sendRestart.bind(this);
    this.post = this.post.bind(this);
    this.snackBarClose = this.snackBarClose.bind(this);


    this.messageQueue = [];

    setInterval(() => {
      this.fetchTorchData()
    }, 50)


    setInterval(() => {
      this.fetchProc()
      this.fetchLogs()
    }, 250)
  }

  notify(message) {
    if (!this.state.shouldAlert) {
      this.setState({
        shouldAlert: true,
        message: message
      });
    } else {
      this.messageQueue.push(message)
    }
  }

  fetchLogs() {
    fetch('/logs').then((resp) => {
      return resp.json()
    }).catch(() => {
    }).then((json) => {
      window.logs = json
    });
  }

  fetchTorchData() {
    fetch('/control').then((resp) => {
      return resp.json()
    }).catch(() => {
      this.setState({connected: false})
      throw new Error()
    }).then((json) => {
      this.setState({connected: true})
      window.torchData = json
    });
  }

  fetchProc() {
    fetch('/proc').then((resp) => {
      return resp.json()
    }).catch(() => {
      this.setState({running: false})
      throw new Error()
    }).then((json) => {
      window.proc = json
      this.setState({running: json['state']})
    });
  }

  post(url, command, cb) {
    fetch('/' + url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(command)
    }).catch(() => {
      this.notify('Error sending JSON command')
    }).then((res) => {
      if (res.status == 200) {
        if (cb)
          cb()
      }
    });
  }

  sendRun() {
    console.log('here')
    this.post('proc', {proc: 'start'})
    this.notify('Starting Torchsong')
  }
  sendStop() {
    this.post('proc', {proc: 'normal_stop'})
    this.notify('Stopping Torchsong')
  }
  sendEstop() {
    this.post('proc', {proc: 'estop'})
    this.notify('Hard stopping Torchsong')
  }
  sendRestart() {
    if (this.state.running) {
      this.post('proc', {proc: 'estop'}, () => {
        setTimeout(() => {
          this.post('proc', {proc: 'start'})
          this.notify('Restarting Torchsong')
        }, 1000)
      })
    }
  }

  snackBarClose() {
    if (this.messageQueue.length == 0) {
      this.setState({
        shouldAlert: false,
        message: ''
      });
    } else {
      this.setState({
        shouldAlert: true,
        message: this.messageQueue.shift()
      });
    }
  }

  render() {
    return (
      <div>
        <AppBar
            title={"Torch Song GUI " + (this.state.running? "(running)" : "(stopped)")}
            showMenuIconButton={false}/>
        <Snackbar open={this.state.shouldAlert} autoHideDuration={1500}
            onRequestClose={this.snackBarClose}
            message={this.state.message} />
        <SongbookPanel notify={this.notify} run={this.sendRun} stop={this.sendStop}
            estop={this.sendEstop} />
        <Tabs>
          <Tab label={"Control"} >
            <div className="control-logs">
              <LogPanel errorsOnly={false} showControls={false} notify={this.notify}/>
            </div>
            <ControlPanel notify={this.notify}/>
          </Tab>
          <Tab label={"Logs"} >
            <LogPanel errorsOnly={false} showControls={true} notify={this.notify}/>
          </Tab>
          <Tab label={"Config"} >
            <YAMLPanel notify={this.notify} restart={this.sendRestart}/>
          </Tab>
        </Tabs>
      </div>
    );
  }
};

const App = () => (
  <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
    <Components />
  </MuiThemeProvider>
);

render(<App/>, document.getElementById('app'));
