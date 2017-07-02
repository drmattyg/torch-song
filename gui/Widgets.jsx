import React from 'react';
import {render} from 'react-dom';

import Toggle from 'material-ui/Toggle';
import Slider from 'material-ui/Slider';
import TextField from 'material-ui/TextField';
import Checkbox from 'material-ui/Checkbox';

export class Label extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <TextField disabled={true} floatingLabelText={this.props.label}
        value={this.props.value} underlineShow={false} />
  }
}

export class SliderWithLabel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.defaultValue
    };
  }
  reset() {
    this.setState({value: this.props.defaultValue});
  }
  render() {
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
};

export class Updater extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    return <TextField disabled={true} floatingLabelText={this.props.label}
        value={this.props.value != undefined ? this.props.value.toFixed(3) : NaN} underlineShow={false} />
  }
};

export class UpdaterBool extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    return <Checkbox disabled={true} label={this.props.label} checked={this.props.value}
        labelStyle={{lineHeight: "24px", fontSize: "12px"}} />
  }
};


export class SimpleToggle extends React.Component{
  constructor(props) {
    super(props);
  }
  render() {
    return <Toggle label={this.props.label} labelPosition="right" style={{padding: "10px"}}
      onToggle={this.props.onToggle} defaultToggled={this.props.defaultToggled || false}
      disabled={this.props.disabled || false} />
  }
};
