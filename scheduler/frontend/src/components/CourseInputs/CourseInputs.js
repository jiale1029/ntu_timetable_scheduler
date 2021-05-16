import React, { useState } from "react";
import Input from "../Input/Input";
import timetableServices from "../../services/timetableServices";
import "./CourseInputs.css";

const CourseInputs = (props) => {
  const [loading, setLoading] = useState(false);
  const [courseCodeInputs, setCourseCodeInputs] = useState([""]);
  const [searchResults, setSearchResults] = useState([
    {
      suggestions: [],
      showSuggestions: false,
    },
  ]);

  const updateCoursesHandler = (evt, id) => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy[id] = evt.target.value.toUpperCase();
    setCourseCodeInputs(courseCodeCopy);
  };

  const queryCourseHandler = async (evt, id) => {
    const userInput = evt.target.value;
    if (userInput.length <= 2) {
      return true;
    }
    const searchResultsCopy = searchResults.slice();

    const results = await timetableServices.queryCourse(userInput);
    searchResultsCopy[id].suggestions = results.data;
    searchResultsCopy[id].showSuggestions = true;
    // TODO: toggle the showSuggestions for each
    setSearchResults(searchResultsCopy);
  };

  const addInputHandler = () => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy.push("");
    const searchResultsCopy = searchResults.slice();
    searchResultsCopy.push({
      suggestions: [],
      showSuggestions: false,
    });
    setCourseCodeInputs(courseCodeCopy);
    setSearchResults(searchResultsCopy);
  };

  const deleteInputHandler = (id) => {
    const courseCodeCopy = courseCodeInputs.slice();
    courseCodeCopy.splice(id, 1);
    const searchResultsCopy = searchResults.slice();
    searchResultsCopy.splice(id, 1);
    setCourseCodeInputs(courseCodeCopy);
    setSearchResults(searchResultsCopy);
  };

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
        name={`courseInput-${idx}`}
        onKeyPress={
          idx === courseCodeInputs.length - 1 ? addInputHandler : undefined
        }
        onChange={(evt) => {
          updateCoursesHandler(evt, idx);
          queryCourseHandler(evt, idx);
        }}
        showSuggestions={searchResults[idx].showSuggestions}
        suggestions={searchResults[idx].suggestions}
        value={c}
      />
      {deleteBtn(courseCodeInputs.length, idx)}
    </li>
  ));

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
