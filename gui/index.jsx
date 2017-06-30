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

class Components extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      logs: [],
      control: {},
      shouldAlert: false,
      message: ''
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

    this.fetchLogs = this.fetchLogs.bind(this);
    this.fetchTorchData = this.fetchTorchData.bind(this);

    setInterval(() => {
      this.fetchTorchData()
    }, 50)


    setInterval(() => {
      this.fetchLogs()
    }, 250)
  }

  fetchLogs() {
    fetch('/logs').then((resp) => {
      return resp.json()
    }).then((json) => {
      window.logs = json
    });
  }

  fetchTorchData() {
    fetch('/control').then((resp) => {
      return resp.json()
    }).then((json) => {
      window.torchData = json
    });
  }

  render() {
    return (
      <div>
        <AppBar title={"Torch Song GUI "}/>
        <Snackbar open={this.state.shouldAlert} autoHideDuration={1000}
            onRequestClose={() => { this.setState({shouldAlert: false}) }}
            message={this.state.message} />
        <Tabs>
          <Tab label={"Control"} >
            <SongbookPanel />
            <ControlPanel />
          </Tab>
          <Tab label={"Logs"} >
            <LogPanel errorsOnly={false} />
          </Tab>
          <Tab label={"YAML parser"} >
            <YAMLPanel />
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
