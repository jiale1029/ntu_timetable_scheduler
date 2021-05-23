import React, { useEffect, useState } from "react";
import Pagination from "@material-ui/lab/Pagination";
import Timetable from "../Timetable/Timetable";
import "./Timetables.css";

const Timetables = (props) => {
  
  const [currentPage, setCurrentPage] = useState(0);

  const renderTimetable = (currentPage) => {
    if (!props.data || currentPage < 1) {
      return true;
    }

    const solutions = props.data;

    // console.log(currentPage);
    const sol = solutions[currentPage-1];
    const joinedKey = Object.values(sol.stats).map((indexNum) => indexNum).join("");

    return <Timetable id={joinedKey} key={joinedKey} data={sol.solutions} />;
    // const timetables = solutions.map((sol) => {
    //   const joinedKey = Object.keys(sol.stats)
    //   .map((indexNum) => indexNum)
    //   .join("_");
      
    //   console.log(joinedKey);
    //   return <Timetable id={joinedKey} key={joinedKey.toString()} data={sol.solutions} />;
    // });

    // return timetables;
  };
  
  useEffect(() => {
    if(props.data && props.data.length > 0){
      setCurrentPage(1);    
    } else {
      setCurrentPage(0);
    }
  }, [props.data]);

  
  let timetable = <Timetable />;
  
  if(currentPage > 0) {
    timetable = renderTimetable(currentPage);
  }

  return (
    <div className="timetables">
      {currentPage !== 0 && <Pagination page={currentPage} onChange={(evt, page) => setCurrentPage(page)} count={props.data.length} siblingCount={1} boundaryCount={1}/>}
      {/* {timetables && timetables[currentPage - 1]} */}
      {timetable && timetable}
    </div>
  );
};

export default Timetables;
