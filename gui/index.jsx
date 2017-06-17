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

class Components extends React.Component {
  render() {
    return (
      <div>
        <AppBar title={"Torch Song GUI "}/>
        <Tabs>
          <Tab label={"Realtime"} >
          </Tab>
          <Tab label={"YAML parser"} >
            <YAMLPanel />
          </Tab>
        </Tabs>
      </div>
    );
  }
  /*
  getInitialState: function() {
    return {};
  },
  componentDidMount: function() {
    var wasConnected = false;
    setInterval(() => {
      fetch('/dbw_state.json').then((resp) => {
        return resp.json()
      }).then((json) => {
        this.setState({dbw_state: json});
        if (!wasConnected) {
          this.setState({shouldAlert: true, connected: true})
        }
        wasConnected = true;
      }).catch(() => {
        if (wasConnected) {
          this.setState({shouldAlert: true, connected: false})
        }
        wasConnected = false;
      })
    }, 100);
  },
  render: function() {
    return (
    <div>
      <Snackbar open={this.state.shouldAlert}
          autoHideDuration={1000}
          onRequestClose={() => { this.setState({shouldAlert: false}) }}
          message={this.state.connected ? "Connected to server" : "Disconnected from server"} />
      <Tabs>
        <Tab label={"DBW GUI Version 1.2.1 (" + (this.state.connected === true ? "Connected" : "Disconnected") + ")"} >
          <div className="card-wrap">
            <FaultAndStatusPanel state={this.state.dbw_state}/>
            <DashIndicatorPanel state={this.state.dbw_state}/>
            <ContactorPanel state={this.state.dbw_state}/>
          </div>
        </Tab>
      </Tabs>
      <Tabs>
        <Tab label="Steering">
          <div className="card-wrap">
            <SteeringPanel0 state={this.state.dbw_state}/>
            <SteeringPanel1 state={this.state.dbw_state}/>
            <SteeringFeedbackPanel state={this.state.dbw_state}/>
          </div>
        </Tab>
        <Tab label="Brakes">
          <div className="card-wrap">
            <BrakePanel0 state={this.state.dbw_state}/>
            <BrakePanel1 state={this.state.dbw_state}/>
            <BTDPanel state={this.state.dbw_state}/>
          </div>
        </Tab>
        <Tab label="Throttle">
          <div className="card-wrap">
            <ThrottlePanelIn state={this.state.dbw_state}/>
            <ThrottlePanelOut state={this.state.dbw_state}/>
          </div>
        </Tab>
        <Tab label="Accessories">
          <div className="card-wrap">
            <LightPanel state={this.state.dbw_state}/>
          </div>
        </Tab>
        <Tab label="Powercard">
          <div className="card-wrap">
            <PowercardMiscPanel state={this.state.dbw_state}/>
          </div>
        </Tab>
      </Tabs>
    </div>
    )
  }
  */
};

const App = () => (
  <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
    <Components />
  </MuiThemeProvider>
);

render(<App/>, document.getElementById('app'));
