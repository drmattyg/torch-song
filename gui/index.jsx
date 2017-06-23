import React from 'react';
import {render} from 'react-dom';

import getMuiTheme from 'material-ui/styles/getMuiTheme';
import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
  
import AppBar from 'material-ui/AppBar';
import {Tabs, Tab} from 'material-ui/Tabs';

/*
import 'whatwg-fetch';
import RaisedButton from 'material-ui/RaisedButton';
import Divider from 'material-ui/Divider';
import Slider from 'material-ui/Slider';
import TextField from 'material-ui/TextField';
import Toggle from 'material-ui/Toggle';
import Paper from 'material-ui/Paper';
import Snackbar from 'material-ui/Snackbar';
*/

// require to make Tabs work
const injectTapEventPlugin = require("react-tap-event-plugin");
injectTapEventPlugin();

const version = process.env.npm_package_version

import {YAMLPanel} from './YAMLParser.jsx';
import {LogPanel} from './LogViewer.jsx';

class Components extends React.Component {
  render() {
    return (
      <div>
        <AppBar title={"Torch Song GUI "}/>
        <Tabs>
          <Tab label={"Control"} >
          </Tab>
          <Tab label={"Logs"} >
            <LogPanel />
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
