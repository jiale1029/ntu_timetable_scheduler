import React, { useEffect } from "react";
import TimetableSlot from "../TimetableSlot/TimetableSlot";
import "./Timetable.css";

const Timetable = (props) => {
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

  const fillTimetable = (timetableDayArray, count) => {
    for (let i = times.length - count; i < times.length; i++) {
      timetableDayArray.push(
        <TimetableSlot
          key={`${props.id}${times[i]}`}
          code=""
          index=""
          group=""
          type=""
          day=""
          venue=""
          time={times[i]}
        />
      );
    }
    return timetableDayArray;
  };

  const renderTimetableSlot = () => {
    const data = props.data;

    const renderedDays = days.map((day) => {
      const dayData = data[day];

      const dayTimetable = [];
      let latestIdx = 0;
      let totalColSpan = times.length;

      dayData.forEach((elem) => {
        let parsedTime = parseTime(elem["Time"]);
        let colSpan = parsedTime.length ? parsedTime.length : 1;

        const currentIdx = times.indexOf(parsedTime[0]);
        // add slots that are empty and no class occupied
        for (let i = latestIdx; i < currentIdx; i++) {
          dayTimetable.push(
            <TimetableSlot
              key={`${props.id}${times[i]}`}
              code=""
              index=""
              group=""
              type=""
              day=""
              venue=""
              time={times[i]}
            />
          );
          totalColSpan -= 1;
        }

        latestIdx = times.indexOf(parsedTime[parsedTime.length - 1]) + 1;

        dayTimetable.push(
          <TimetableSlot
            key={`${props.id}${times[latestIdx - colSpan]}`}
            colSpan={colSpan}
            code={elem.Code}
            index={elem.Index}
            group={elem.Group}
            type={elem.Type}
            day={elem.Day}
            venue={elem.Venue}
            time={elem.Time}
          />
        );
        totalColSpan -= colSpan;
      });
      fillTimetable(dayTimetable, totalColSpan);

      return dayTimetable;
    });
    return renderedDays;
  };

  const timetableSlot = renderTimetableSlot();

  return (
    <div>
      <table>
        <tbody>
          <tr>
            <th>Time</th>
            <th>0800-0830</th>
            <th>0830-0900</th>
            <th>0900-0930</th>
            <th>0930-1000</th>
            <th>1000-1030</th>
            <th>1030-1100</th>
            <th>1100-1130</th>
            <th>1130-1200</th>
            <th>1200-1230</th>
            <th>1230-1300</th>
            <th>1300-1330</th>
            <th>1330-1400</th>
            <th>1400-1430</th>
            <th>1430-1500</th>
            <th>1500-1530</th>
            <th>1530-1600</th>
            <th>1600-1630</th>
            <th>1630-1700</th>
            <th>1700-1730</th>
            <th>1730-1800</th>
            <th>1800-1830</th>
            <th>1830-1900</th>
            <th>1900-1930</th>
            <th>1930-2000</th>
            <th>2000-2030</th>
            <th>2030-2100</th>
            <th>2100-2130</th>
            <th>2130-2200</th>
            <th>2200-2230</th>
            <th>2230-2300</th>
            <th>2300-2330</th>
          </tr>
          <tr>
            <th>Monday</th>
            {timetableSlot[0]}
          </tr>
          <tr>
            <th>Tuesday</th>
            {timetableSlot[1]}
          </tr>
          <tr>
            <th>Wednesday</th>
            {timetableSlot[2]}
          </tr>
          <tr>
            <th>Thursday</th>
            {timetableSlot[3]}
          </tr>
          <tr>
            <th>Friday</th>
            {timetableSlot[4]}
          </tr>
          <tr>
            <th>Saturday</th>
            {timetableSlot[5]}
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Timetable;
