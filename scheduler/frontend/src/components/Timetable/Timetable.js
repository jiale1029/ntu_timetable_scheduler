import React, { useEffect } from "react";
import ReactDOM from "react-dom"
import {
  Paper,
  TableContainer,
  Table,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import TimetableSlot from "../TimetableSlot/TimetableSlot";
import "./Timetable.css";

const Timetable = (props) => {
  console.log("rendering single timetable");

  const days = ["mon", "tue", "wed", "thu", "fri", "sat"];
  const times = [
    "0800",
    "0830",
    "0900",
    "0930",
    "1000",
    "1030",
    "1100",
    "1130",
    "1200",
    "1230",
    "1300",
    "1330",
    "1400",
    "1430",
    "1500",
    "1530",
    "1600",
    "1630",
    "1700",
    "1730",
    "1800",
    "1830",
    "1900",
    "1930",
    "2000",
    "2030",
    "2100",
    "2130",
    "2200",
    "2230",
    "2300",
  ];

  const parseTime = (timeRange) => {
    const [start, end] = timeRange.split("-");
    const startIdx = times.indexOf(start);
    const endIdx = times.indexOf(end);
    return times.slice(startIdx, endIdx);
  };

  const useStyles = makeStyles({
    table: {
      minHeight: 600,
    },
    tableCell: {
      position: '-webkit-sticky',
      position: 'sticky',
      background: '#fff',
      left: 0,
      zIndex: 1,
    }
  });

  // fill the remaining tail slots
  // const fillTimetable = (timetableDayArray, count) => {
  //   for (let i = times.length - count; i < times.length; i++) {
  //     timetableDayArray.push(
  //       <TimetableSlot
  //         key={`${props.id}${i}`}
  //         code=""
  //         index=""
  //         group=""
  //         type=""
  //         day=""
  //         venue=""
  //         time={times[i]}
  //       />
  //     );
  //   }
  //   return timetableDayArray;
  // };

  // // render timeslots for each day
  // const renderTimetableSlot = () => {
  //   const data = props.data;

  //   const renderedDays = days.map((day) => {
  //     const dayData = data[day];

  //     const dayTimetable = [];
  //     let latestIdx = 0;
  //     let totalColSpan = times.length;

  //     dayData.forEach((elem) => {
  //       let parsedTime = parseTime(elem["Time"]);
  //       let colSpan = parsedTime.length ? parsedTime.length : 1;

  //       const currentIdx = times.indexOf(parsedTime[0]);
  //       // add slots that are empty and no class occupied
  //       for (let i = latestIdx; i < currentIdx; i++) {
  //         dayTimetable.push(
  //           <TimetableSlot
  //             key={`${props.id}${times[i]}`}
  //             // key={`${props.id}${i}`}
  //             code=""
  //             index=""
  //             group=""
  //             type=""
  //             day=""
  //             venue=""
  //             time={times[i]}
  //           />
  //         );
  //         totalColSpan -= 1;
  //       }

  //       latestIdx = times.indexOf(parsedTime[parsedTime.length - 1]) + 1;

  //       // fill the class timeslot after empty slot are done
  //       dayTimetable.push(
  //         <TimetableSlot
  //           key={`${props.id}${times[latestIdx - colSpan]}`}
  //           colSpan={colSpan}
  //           code={elem.Code}
  //           index={elem.Index}
  //           group={elem.Group}
  //           type={elem.Type}
  //           day={elem.Day}
  //           venue={elem.Venue}
  //           time={elem.Time}
  //         />
  //       );
  //       totalColSpan -= colSpan;
  //     });
  //     fillTimetable(dayTimetable, totalColSpan);

  //     return dayTimetable;
  //   });
  //   return renderedDays;
  // };

  // const timetableSlot = renderTimetableSlot();
  const classes = useStyles();

  // return (
  //   <TableContainer component={Paper}>
  //     <Table stickyHeader aria-label="sticky table" className={classes.table} size="small">
  //       <TableHead>
  //         <TableRow>
  //           {/* <TableCell>0800-0830</TableCell>
  //           <TableCell>0830-0900</TableCell>
  //           <TableCell>0900-0930</TableCell>
  //           <TableCell>0930-1000</TableCell>
  //           <TableCell>1000-1030</TableCell>
  //           <TableCell>1030-1100</TableCell>
  //           <TableCell>1100-1130</TableCell>
  //           <TableCell>1130-1200</TableCell>
  //           <TableCell>1200-1230</TableCell>
  //           <TableCell>1230-1300</TableCell>
  //           <TableCell>1300-1330</TableCell>
  //           <TableCell>1330-1400</TableCell>
  //           <TableCell>1400-1430</TableCell>
  //           <TableCell>1430-1500</TableCell>
  //           <TableCell>1500-1530</TableCell>
  //           <TableCell>1530-1600</TableCell>
  //           <TableCell>1600-1630</TableCell>
  //           <TableCell>1630-1700</TableCell>
  //           <TableCell>1700-1730</TableCell>
  //           <TableCell>1730-1800</TableCell>
  //           <TableCell>1800-1830</TableCell>
  //           <TableCell>1830-1900</TableCell>
  //           <TableCell>1900-1930</TableCell>
  //           <TableCell>1930-2000</TableCell>
  //           <TableCell>2000-2030</TableCell>
  //           <TableCell>2030-2100</TableCell>
  //           <TableCell>2100-2130</TableCell>
  //           <TableCell>2130-2200</TableCell>
  //           <TableCell>2200-2230</TableCell>
  //           <TableCell>2230-2300</TableCell>
  //           <TableCell>2300-2330</TableCell> */}
  //           <TableCell></TableCell>
  //           <TableCell>0800</TableCell>
  //           <TableCell>0830</TableCell>
  //           <TableCell>0900</TableCell>
  //           <TableCell>0930</TableCell>
  //           <TableCell>1000</TableCell>
  //           <TableCell>1030</TableCell>
  //           <TableCell>1100</TableCell>
  //           <TableCell>1130</TableCell>
  //           <TableCell>1200</TableCell>
  //           <TableCell>1230</TableCell>
  //           <TableCell>1300</TableCell>
  //           <TableCell>1330</TableCell>
  //           <TableCell>1400</TableCell>
  //           <TableCell>1430</TableCell>
  //           <TableCell>1500</TableCell>
  //           <TableCell>1530</TableCell>
  //           <TableCell>1600</TableCell>
  //           <TableCell>1630</TableCell>
  //           <TableCell>1700</TableCell>
  //           <TableCell>1730</TableCell>
  //           <TableCell>1800</TableCell>
  //           <TableCell>1830</TableCell>
  //           <TableCell>1900</TableCell>
  //           <TableCell>1930</TableCell>
  //           <TableCell>2000</TableCell>
  //           <TableCell>2030</TableCell>
  //           <TableCell>2100</TableCell>
  //           <TableCell>2130</TableCell>
  //           <TableCell>2200</TableCell>
  //           <TableCell>2230</TableCell>
  //           <TableCell>2300</TableCell>
  //         </TableRow>
  //       </TableHead>
  //       <TableBody>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Mon</TableCell>
  //           {timetableSlot[0]}
  //         </TableRow>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Tues</TableCell>
  //           {timetableSlot[1]}
  //         </TableRow>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Wed</TableCell>
  //           {timetableSlot[2]}
  //         </TableRow>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Thurs</TableCell>
  //           {timetableSlot[3]}
  //         </TableRow>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Fri</TableCell>
  //           {timetableSlot[4]}
  //         </TableRow>
  //         <TableRow>
  //           <TableCell className={classes.tableCell}>Sat</TableCell>
  //           {timetableSlot[5]}
  //         </TableRow>
  //       </TableBody>
  //     </Table>
  //   </TableContainer>
  // );

  const renderTimetableSlots = () => {
    if(!props.data){
      return true;
    }
    const element = <div class="slot">testing first</div>
    ReactDOM.render(element, document.getElementById("timetable-slot-monday-0830"));
    ReactDOM.render(element, document.getElementById("timetable-slot-wednesday-0930"));
  }
  
  useEffect(() => {
    renderTimetableSlots();
  }, [props.data]);
  
  const tableHeaders = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
  return (
    <div id="your-table">
      {
        tableHeaders.map((tableHeader, idx) => {
          const columnKey = `timetable-column-${idx}`;
          const headerKey = `timetable-header-${tableHeader.toLowerCase()}`;
          return (
            <div class="timetable-column" key={columnKey}>
              <span class="timetable-header" key={headerKey}>{tableHeader.toLowerCase()}</span>
              {
                times.map(time => {
                  const timeslotKey = `timetable-slot-${tableHeader.toLowerCase()}-${time}`;
                  return <span id={timeslotKey} key={timeslotKey}>{idx === 0? time: ""}</span>;
                })
              }
            </div>
          )
        })
      }
    </div>
  )
};

export default Timetable;
