import React from "react";

const TimetableSlot = (props) => {
  return (
    <div>
      <ul>
        <li>{props.code}</li>
        <li>{props.index}</li>
        <li>{props.group}</li>
        <li>{props.type}</li>
        <li>{props.day}</li>
        <li>{props.time}</li>
        <li>{props.venue}</li>
      </ul>
    </div>
  );
};

export default TimetableSlot;
