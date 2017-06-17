import React from 'react';
import {render} from 'react-dom';

import {SimpleToggle, Label, SliderWithLabel, Updater, UpdaterBool} from './Widgets.jsx';
import Paper from 'material-ui/Paper';
import Toggle from 'material-ui/Toggle';

var post = function(name_, value_) {
  fetch('post', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name_,
      value:value_,
    })
  })
};

export const SteeringFeedbackPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Torque and Encoder Sensors</h2>
          <Updater value={this.props.state.torque1_a} label="Torque 1A voltage"/>
          <Updater value={this.props.state.torque1_b} label="Torque 1B voltage"/>
          <Updater value={this.props.state.torque2_a} label="Torque 2A voltage"/>
          <Updater value={this.props.state.torque2_b} label="Torque 2B voltage"/>
          <UpdaterBool value={this.props.state.torque_a_fault} label="Torque A fault"/>
          <UpdaterBool value={this.props.state.torque_b_fault} label="Torque B fault"/>
          <Updater value={this.props.state.encoder0} label="Encoder 1"/>
          <Updater value={this.props.state.encoder1} label="Encoder 2"/>
          <Updater value={this.props.state.encoder2} label="Encoder 3"/>
        </Paper>
      </div>
    )
  }
});

export const SteeringPanel0 = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Steering 1 System</h2>
          <SliderWithLabel ref="slider" defaultValue={0} min={0} max={1} label="Duty Cycle" onChange={(e, arg) => {
              post("steering0_pwm_dc", arg);
          }} />
          <SimpleToggle label="Inhibit" defaultToggled={true} onToggle={(e, arg) => {
              if (arg === true) {
                this.refs.slider.reset();
                post("steering0_pwm_dc", 0);
              }
              post("steering0_inhibit", arg);
          }} />
          <SimpleToggle label="Direction"
            onToggle={(e, arg) => { post("steering0_direction", arg) }} />
          <Updater value={this.props.state.steer_current_a} label="Current (A)"/>
          <UpdaterBool value={this.props.state.steering_fault_a} label="Fault"/>
        </Paper>
      </div>
    )
  }
});

export const SteeringPanel1 = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Steering 2 System</h2>
          <SliderWithLabel ref="slider" defaultValue={0} min={0} max={1} label="Duty Cycle" onChange={(e, arg) => {
              post("steering1_pwm_dc", arg);
          }} />
          <SimpleToggle label="Inhibit" defaultToggled={true} onToggle={(e, arg) => {
              if (arg === true) {
                this.refs.slider.reset();
                post("steering1_pwm_dc", 0);
              }
              post("steering1_inhibit", arg);
          }} />
          <SimpleToggle label="Direction"
            onToggle={(e, arg) => { post("steering1_direction", arg) }} />
          <Updater value={this.props.state.steer_current_a} label="Current (A)"/>
          <UpdaterBool value={this.props.state.steering_fault_a} label="Fault"/>
        </Paper>
      </div>
    )
  }
});

export const LightPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Turn Signals</h2>
          <SimpleToggle label="Right Signal"
            onToggle={(e, arg) => { post("signal_right", arg) }} />
          <SimpleToggle label="Left Signal"
            onToggle={(e, arg) => { post("signal_left", arg) }} />
          <SimpleToggle label="Hazard Signal"
            onToggle={(e, arg) => { post("signal_hazard", arg) }} />
        </Paper>
      </div>
    )
  }
});

export const BrakePanel0 = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Front Brake System</h2>
          <SliderWithLabel ref="slider" defaultValue={0} min={0} max={1} label="Duty Cycle" onChange={(e, arg) => {
              post("brake0_pwm_dc", arg);
          }} />
          <SimpleToggle label="Inhibit" defaultToggled={true} onToggle={(e, arg) => {
              if (arg === true) {
                this.refs.slider.reset();
                post("brake0_pwm_dc", 0);
              }
              post("brake0_inhibit", arg);
          }} />
          <Updater value={this.props.state.brake_pressure_a2} label="Secondary Brake Supply Output"/>
          <Updater value={this.props.state.brake_pressure_a1} label="Secondary Brake Supply Source"/>
          <Updater value={this.props.state.brake_current_a} label="Current (A)"/>
          <UpdaterBool updater={this.props.state.brake_fault_a} label="Fault"/>

        </Paper>
      </div>
    )
  }
});

export const BrakePanel1 = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Rear Brake System</h2>
          <SliderWithLabel ref="slider" defaultValue={0} min={0} max={1} label="Duty Cycle" onChange={(e, arg) => {
              post("brake1_pwm_dc", arg);
          }} />
          <SimpleToggle label="Inhibit" defaultToggled={true} onToggle={(e, arg) => {
              if (arg === true) {
                this.refs.slider.reset();
                post("brake1_pwm_dc", 0);
              }
              post("brake1_inhibit", arg);
          }} />
          <Updater value={this.props.state.brake_pressure_b2} label="Primary Brake Supply Output"/>
          <Updater value={this.props.state.brake_pressure_b1} label="Primary Brake Supply Source"/>
          <Updater value={this.props.state.brake_current_b} label="Current (A)"/>
          <UpdaterBool value={this.props.state.brake_fault_b} label="Fault"/>
        </Paper>
      </div>
    )
  }
});


export const ThrottlePanelIn = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Throttle Input </h2>
          <Updater value={this.props.state.ecu5v} label="ECU 5V"/>
          <Updater value={this.props.state.pedal_aps1_in} label="APS 1"/>
          <Updater value={this.props.state.pedal_aps2_in} label="APS 2"/>
          <UpdaterBool value={this.props.state.pedal_ivs_in} label="IVS"/>
        </Paper>
      </div>
    )
  }
});

export const ThrottlePanelOut = React.createClass({
  generateThrottleSignals: function(perc) {
    var lerp = function(val, min, max, low, high) {
      if (val < min) { return low }
      else if (val >= max) { return high}
      else {
        var frac = (val - min) / (max - min);
        return (high - low) * frac + low;
      }
    };
    var ivs = perc > 15;
    var aps1 = lerp(perc, 8, 72, 0.5, 3.1);
    var aps2 = lerp(perc, 0, 38, 3.1, 0.5);

    post("pedal_aps1_out", aps1);
    post("pedal_aps2_out", aps2);
    post("pedal_ivs_spoof", ivs);
  },
  getInitialState: function() {
    return {mode: false};
  },
  componentDidMount: function() {
    this.setState({mode: false});
  },
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Throttle Spoof</h2>
          <SimpleToggle label="Throttle Mode"
            onToggle={ (e, arg) => {
              this.setState({mode: arg});
            }} />
          <SimpleToggle label="Throttle Spoof"
            onToggle={ (e, arg) => {
              post("throttle_spoof_enable", arg);
            }} />
          <div style={{display: this.state.mode === false ? "none" : "block"}}>
            <SliderWithLabel defaultValue = {0} min={0} max={100} label="Throttle Control"
              onChange={(e, arg) => this.generateThrottleSignals(arg)} />
          </div>
          <div style={{display: this.state.mode === false ? "block" : "none"}}>
            <SliderWithLabel defaultValue = {0} min={0} max={5} label="APS 1 Spoof"
              onChange={(e, arg) => post("pedal_aps1_out", arg)} />
            <SliderWithLabel defaultValue = {0} min={0} max={5} label="APS 2 Spoof"
              onChange={(e, arg) => post("pedal_aps2_out", arg)} />
            <SimpleToggle label="IVS Spoof"
              onToggle={ (e, arg) => { post("pedal_ivs_spoof", arg) }} />
          </div>
        </Paper>
      </div>
    )
  }
});


export const FaultAndStatusPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Fault and Status</h2>
            <UpdaterBool value={this.props.state.estop} label="Estop"/>
            <UpdaterBool value={this.props.state.fault_in} label="Input fault"/>
            <UpdaterBool value={this.props.state.watchdog_fault} label="Watchdog fault"/>
            <SimpleToggle label="Watchdog latch clear"
              onToggle={ (e, arg) => { post("watchdog_latch_clear", arg) }} />
            <SimpleToggle label="Force fault"
              onToggle={ (e, arg) => { post("fault_out", arg) }} />
            <Updater value={this.props.state.board_id} label="Board rev"/>
            <UpdaterBool value={this.props.state.powercard} label="Powercard present"/>
        </Paper>
      </div>
    )
  }
});

export const DashIndicatorPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Dash Indicator</h2>
            <UpdaterBool value={this.props.state.dash_engage} label="Dash engage"/>
            <SimpleToggle label="Dash software ready"
              onToggle={ (e, arg) => { post("dash_sw_ready", arg) }} />
        </Paper>
      </div>
    )
  }
});



export const ContactorPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Contactor</h2>
          <Updater value={this.props.state.pre_contactor_sense} label="Pre-contactor voltage"/>
          <Updater value={this.props.state.post_contactor_sense} label="Post-contactor voltage"/>
          <SimpleToggle label="Pre-charge"
            onToggle={ (e, arg) => { post("contactor_precharge", arg) }} />
          <SimpleToggle label="Contactor"
            onToggle={ (e, arg) => { post("contactor", arg) }} />
        </Paper>
      </div>
    )
  }
});


export const BTDPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <UpdaterBool value={this.props.state.brake_disconnect_in}
            label="BTD In"/>
          <SimpleToggle label="BTD Spoof"
            onToggle={ (e, arg) => { post("brake_disconnect_spoof", arg) }} />
        </Paper>
      </div>
    )
  }
});

export const PowercardBrakePanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Powercard Signals</h2>
          <Updater value={this.props.state.brake_current_a} label="Brake Current A (A)"/>
          <UpdaterBool value={this.props.state.brake_fault_a} label="Brake Fault A"/>
          <Updater value={this.props.state.brake_current_b} label="Brake Current B (A)"/>
          <UpdaterBool value={this.props.state.brake_fault_b} label="Brake Fault B"/>
        </Paper>
      </div>
    )
  }
});

export const PowercardSteeringPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Powercard Signals</h2>
          <Updater value={this.props.state.steer_current_a} label="Brake Current A (A)"/>
          <UpdaterBool value={this.props.state.steer_fault_a} label="Brake Fault A"/>
          <Updater value={this.props.state.steer_current_b} label="Brake Current B (A)"/>
          <UpdaterBool value={this.props.state.steer_fault_b} label="Brake Fault B"/>
        </Paper>
      </div>
    )
  }
});

export const PowercardMiscPanel = React.createClass({
  render: function() {
    return (
      <div className="material-ui-wrap">
        <Paper style={{padding: "10px"}}>
          <h2>Powercard Signals</h2>
          <Updater value={this.props.state.driver_temperature} label="Driver temperature"/>
          <Updater value={this.props.state.pcb_temperature} label="PCB temperature"/>
          <Updater value={this.props.state.input_current_a} label="Input A Current (A)"/>
          <Updater value={this.props.state.input_current_b} label="Input B Current (A)"/>
        </Paper>
      </div>
    )
  }
});

