import React, { useState } from "react";
import Input from "../Input/Input";
import timetableServices from "../../services/timetableServices";
import "./CourseInputs.css";

const useRenderInputs = (courseCodeInputs, setCourseCodeInputs) => {
  const updateCoursesHandler = (evt, id) => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy[id] = evt.target.value.toUpperCase();
    setCourseCodeInputs(courseCodeCopy);
  };

  const queryCourseHandler = async (evt) => {
    const userInput = evt.target.value;
    if (userInput.length <= 2) return true;

    const searchResults = await timetableServices.queryCourse(userInput);
  };

  const addInputHandler = () => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy.push("");
    setCourseCodeInputs(courseCodeCopy);
  };

  const deleteInputHandler = (id) => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy.splice(id, 1);
    setCourseCodeInputs(courseCodeCopy);
  };

  const deleteBtn = (arrayLength, idx) => {
    return arrayLength === 1 ? (
      ""
    ) : (
      <button type="button" onClick={() => deleteInputHandler(idx)}>
        -
      </button>
    );
  };

  const inputs = courseCodeInputs.map((c, idx) => (
    <li key={idx}>
      <Input
        onKeyPress={
          idx === courseCodeInputs.length - 1 ? addInputHandler : undefined
        }
        onChange={(evt) => {
          updateCoursesHandler(evt, idx);
        }}
        onKeyDown={(evt) => {
          queryCourseHandler(evt);
        }}
        value={c}
      />
      {deleteBtn(courseCodeInputs.length, idx)}
    </li>
  ));

  return inputs;
};

const CourseInputs = (props) => {
  const [loading, setLoading] = useState(false);
  const [courseCodeInputs, setCourseCodeInputs] = useState([""]);
  const inputs = useRenderInputs(courseCodeInputs, setCourseCodeInputs);

  const queryClickHandler = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const courseCodesFiltered = new Set(
        courseCodeInputs.filter((courseCode) => courseCode !== "")
      );

      const respBody = await timetableServices.getTimetables([
        ...courseCodesFiltered,
      ]);
      const respData = respBody.data;
      props.callbackFromParent(respData);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form>
        <ul>
          <li>
            <button id="queryBtn" type="submit" onClick={queryClickHandler}>
              {loading ? "Loading..." : "Query Possible Timetables!"}
            </button>
          </li>
          {inputs}
        </ul>
      </form>
    </div>
  );
};

export default CourseInputs;
