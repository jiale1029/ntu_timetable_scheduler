import React, { useState } from "react";
import CourseInputs from "../CourseInputs/CourseInputs";
import Timetables from "../Timetables/Timetables";

const MainPage = () => {
  const [timetableData, setTimetableData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);


  const callbackRetrieveTimetableData = (data) => {
    setTimetableData(data.class);
    setCurrentPage(0);
  };

  return (
    <div>
      <Timetables
        data={timetableData}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
      />
      <CourseInputs callbackFromParent={callbackRetrieveTimetableData} />
    </div>
  );
};

export default MainPage;
