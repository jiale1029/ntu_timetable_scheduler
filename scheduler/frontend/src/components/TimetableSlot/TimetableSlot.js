import React from "react";
import { TableCell, List, ListItem, ListItemText } from "@material-ui/core";
import "./TimetableSlot.css";

const TimetableSlot = (props) => {
  return (
    <TableCell colSpan={props.colSpan} key={`${props.id}`}>
      <List dense={true} disablePadding={true}>
        <ListItem dense={true} disableGutters={true}>
          <ListItemText
            primaryTypographyProps={{ style: { whiteSpace: "normal" } }}
            primary={props.code}
          />
        </ListItem>
        <ListItem dense={true} disableGutters={true}>
          <ListItemText
            primaryTypographyProps={{ style: { whiteSpace: "normal" } }}
            primary={props.group}
          />
        </ListItem>
        <ListItem dense={true} disableGutters={true}>
          <ListItemText
            primaryTypographyProps={{ style: { whiteSpace: "normal" } }}
            primary={props.type}
          />
        </ListItem>
        <ListItem dense={true} disableGutters={true}>
          <ListItemText
            primaryTypographyProps={{ style: { whiteSpace: "normal" } }}
            primary={props.venue}
          />
        </ListItem>
      </List>
    </TableCell>
  );
};

export default TimetableSlot;
