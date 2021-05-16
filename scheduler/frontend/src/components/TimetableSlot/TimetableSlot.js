import React from "react";
import "./TimetableSlot.css";

const TimetableSlot = (props) => {
  return (
    <td className="course" colSpan={props.colSpan}>
      <ul>
        <li>{props.code}</li>
        <li>{props.index}</li>
        <li>{props.group}</li>
        <li>{props.type}</li>
        <li>{props.day}</li>
        <li>{props.time}</li>
        <li>{props.venue}</li>
      </ul>
    </td>
  );
};

export default TimetableSlot;
