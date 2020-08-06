import api from "../utils/api";

const getCourse = async (courseCode) => api.get(`/courses/${courseCode}`);

const getCourses = async () => api.get("/courses");

const getTimetables = async (courseCodes) => {
  const queryArray = courseCodes.map(
    (courseCode) => `course_code=${courseCode}`
  );
  const queryString = queryArray.join("&");
  return api.get(`/timetables?${queryString}`);
};

const queryCourse = async (userInput) => {
  return api.get(`/course/search?query=${userInput}`);
};

export default {
  getCourse,
  getCourses,
  getTimetables,
  queryCourse,
};
