import React from 'react';
import {render} from 'react-dom';

import Toggle from 'material-ui/Toggle';
import Slider from 'material-ui/Slider';
import TextField from 'material-ui/TextField';
import Checkbox from 'material-ui/Checkbox';

export const Label = React.createClass({
  render: function() {
    return <TextField disabled={true} floatingLabelText={this.props.label}
        value={this.props.value} underlineShow={false} />
  }
});

export const SliderWithLabel = React.createClass({
  getInitialState: function() {
    return { value: this.props.defaultValue }
  },
  reset: function() {
    this.setState({value: this.props.defaultValue});
  },
  render: function() {
    return (
      <div>
        <Label label={this.props.label} value={this.state.value} />
        <Slider value={this.state.value} min={this.props.min} max={this.props.max}
            style={{marginTop: "0px", marginBottom: "0px"}} onChange={ (e, arg) => {
          this.setState({value: arg});
          this.props.onChange(e, arg);
        }}/>
      </div>
    )
  }
});

export const Updater = React.createClass({
  render: function() {
    return <TextField disabled={true} floatingLabelText={this.props.label}
        value={this.props.value != undefined ? this.props.value.toFixed(3) : NaN} underlineShow={false} />
  }
});

export const UpdaterBool = React.createClass({
  render: function() {
    return <Checkbox disabled={true} label={this.props.label} checked={this.props.value}
        labelStyle={{lineHeight: "24px", fontSize: "12px"}} />
  }
});


export const SimpleToggle = React.createClass({
  render: function() {
    return <Toggle label={this.props.label} labelPosition="right" style={{padding: "10px"}}
      onToggle={this.props.onToggle} defaultToggled={this.props.defaultToggled || false} />
    
  }
});
