import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import SearchIcon from "@material-ui/icons/Search";
import Divider from "@material-ui/core/Divider";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";

import Input from "../Input/Input";
import timetableServices from "../../services/timetableServices";
import "./CourseInputs.css";

const CourseInputs = (props) => {
  const [loading, setLoading] = useState(false);

  const [courseCodeInputs, setCourseCodeInputs] = useState([
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
  ]);
  const [searchResults, setSearchResults] = useState([
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
    {
      suggestions: [],
    },
  ]);

  const updateCoursesHandler = (id, value, reason) => {
    if (reason === "select-option"){
      setCourseCodeInputs((prevCourseCodeInputs) => {
        prevCourseCodeInputs[id] = value.Code.toUpperCase();
        return [...prevCourseCodeInputs];
      });
    } else if (reason === "clear"){
      setCourseCodeInputs((prevCourseCodeInputs) => {
        prevCourseCodeInputs[id] = "";
        return [...prevCourseCodeInputs];
      })
    }
  };

  // Query course on typing
  const queryCourseHandler = async (id, value, reason) => {
    if(reason === "reset"){
      setSearchResults((prevResults) => {
        prevResults[id].suggestions = [];
        return [...prevResults];
      });

      return true;
    }
    // only query if length > 2
    if (value.length <= 2)
      return true;

    if (reason === "input"){
      // only query when user is typing, not selecting one of the suggestions
      const userInput = value.toUpperCase();
      const results = await timetableServices.queryCourse(userInput);

      setSearchResults((prevSearchResults) => {
        prevSearchResults[id].suggestions = results.data;
        return [...prevSearchResults]
      });
      return true;
    }
  };

  const queryClickHandler = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      // filter any empty entry
      const courseCodesFiltered = new Set(
        courseCodeInputs.filter((courseCode) => courseCode !== "")
      );

      if (courseCodesFiltered.size > 0) {
        // query backend for the course details
        const respBody = await timetableServices.getTimetables([
          ...courseCodesFiltered,
        ]);
        const respData = respBody.data;
        props.setTimetableData(respData.class);
        props.setOpen(false);
      }
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const inputs = courseCodeInputs.map((c, idx) => (
    <ListItem key={idx}>
      <Input
        name={`courseInput-${idx}`}
        courseInputIdx={idx}
        onChangeHandler={updateCoursesHandler}
        onInputChangeHandler={queryCourseHandler}
        suggestions={searchResults[idx].suggestions}
      />
      <Divider />
    </ListItem>
  ));

  return (
    <div>
      <form>
        <List>
          <ListItem>
            <Button
              id="queryBtn"
              type="submit"
              onClick={queryClickHandler}
              variant="contained"
              color="primary"
              size="large"
              endIcon={<SearchIcon />}
            >
              {loading ? "Loading..." : "Query"}
            </Button>
          </ListItem>
          {inputs}
        </List>
      </form>
    </div>
  );
};

export default CourseInputs;
