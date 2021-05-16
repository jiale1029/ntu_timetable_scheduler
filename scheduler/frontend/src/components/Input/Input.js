import React from "react";
import "./Input.css";

const Input = (props) => {
  const onKeyPress = props.onKeyPress;
  const onChange = props.onChange;
  const onFocus = props.onFocus;
  const value = props.value;
  const name = props.name;

  const suggestionListComponent = () => {
    if (value) {
      console.log(props.showSuggestions);
      console.log(props.suggestions);
      if (props.showSuggestions && props.suggestions.length) {
        return (
          <ul>
            {props.suggestions.map((suggestion, idx) => {
              return (
                <li
                  key={`${suggestion.Code} ${suggestion.Title}`}
                >{`${suggestion.Code} ${suggestion.Title}`}</li>
              );
            })}
          </ul>
        );
      }

      return (
        <div>
          <em>No course is found!</em>
        </div>
      );
    }
  };

  return (
    <>
      <input
        name={name}
        onKeyPress={onKeyPress}
        onChange={onChange}
        onFocus={onFocus}
        value={value}
      />
      {suggestionListComponent()}
    </>
  );
};

export default Input;
