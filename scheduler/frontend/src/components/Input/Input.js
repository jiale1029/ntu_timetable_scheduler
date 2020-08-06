import React from "react";
import "./Input.css";

const Input = (props) => {
  const onKeyPress = props.onKeyPress;
  const onChange = props.onChange;
  const value = props.value;

  return <input onKeyPress={onKeyPress} onChange={onChange} value={value} />;
};

export default Input;
