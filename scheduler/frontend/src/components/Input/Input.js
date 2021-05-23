import React, { useState } from "react";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import "./Input.css";


const Input = (props) => {
  const onInputChangeHandler = props.onInputChangeHandler;
  const onChangeHandler = props.onChangeHandler;
  const courseInputIdx = props.courseInputIdx;

  return (
    <>
      <Autocomplete
        id="combo-box-demo"
        options={props.suggestions}
        getOptionLabel={(suggestion) => {if(suggestion && suggestion.Code) return suggestion.Code + " " + suggestion.Title; else return "";}}
        style={{ width: 300 }}
        onInputChange={(evt, value, reason) => onInputChangeHandler(courseInputIdx, value, reason)}
        onChange={(evt, value, reason) => onChangeHandler(courseInputIdx, value, reason)}
        renderInput={(params) => <TextField {...params} label="Search for your course" variant="outlined" />}
        getOptionSelected={(option, value) => option.id === value.id}
      />
    </>
  );
};

export default Input;
