import React, { useEffect, useState } from "react";
import Timetable from "../Timetable/Timetable";
import "./Timetables.css";

const Timetables = (props) => {
  const currentPage = props.currentPage;
  const setCurrentPage = props.setCurrentPage;

  const renderTimetable = () => {
    if (!props.data.class) {
      return "";
    }

    const solutions = props.data.class;

    const timetables = solutions.map((sol) => {
      const joinedKey = Object.values(sol.stats)
        .map((indexNum) => indexNum)
        .join("");

      return <Timetable id={joinedKey} key={joinedKey} data={sol.solutions} />;
    });

    return timetables;
  };

  const renderPageBtn = (timetables) => {
    const pageElem = (
      <p>
        {currentPage}/{timetables.length}
      </p>
    );

    const prevBtn = (
      <button type="button" onClick={() => setCurrentPage(currentPage - 1)}>
        Previous Page
      </button>
    );

    const nextBtn = (
      <button type="button" onClick={() => setCurrentPage(currentPage + 1)}>
        Next Page
      </button>
    );

    if (!timetables) {
      return "";
    }

    if (currentPage + 1 > timetables.length) {
      return (
        <div>
          {prevBtn}
          {pageElem}
        </div>
      );
    }

    if (currentPage - 1 === 0) {
      return (
        <div>
          {pageElem}
          {nextBtn}
        </div>
      );
    }
    return (
      <div>
        {prevBtn}
        {pageElem}
        {nextBtn}
      </div>
    );
  };

  const timetables = renderTimetable();
  const pageBtn = renderPageBtn(timetables);

  useEffect(() => {
    if (currentPage === 0) {
      setCurrentPage(1);
    }
  }, [timetables]);

  return (
    <div className="timetables">
      {timetables && <div>{pageBtn}</div>}
      {timetables && timetables[currentPage - 1]}
    </div>
  );
};

export default Timetables;
