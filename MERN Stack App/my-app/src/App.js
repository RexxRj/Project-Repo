import "./App.css";
import React, { useState } from "react";
import GoalList from "./components/GoalList/GoalList";
import NewGoal from "./components/NewGoal/NewGoal";

function App() {
  const [courseGoals, setCourseGoals] = useState([
    { id: "cg1", text: "Finish the Course" },
    { id: "cg2", text: "Learn all about the Course Main Topic" },
    { id: "cg3", text: "Help in Q&A" },
  ]);

  const addGoalHandler = (newGoal) => {
    //if prevstates are not interdependent use this, as order may get changed
    //setCourseGoals(courseGoals.concat(newGoal));
    setCourseGoals((prevCourseGoals) => prevCourseGoals.concat(newGoal));
  };

  return (
    <div className="App">
      <h2>Course Goals</h2>
      <NewGoal onAddGoal={addGoalHandler} />
      <GoalList goals={courseGoals} />
    </div>
  );
}

export default App;
