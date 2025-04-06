import "./App.css";
import React from "react";
import {
  Route,
  BrowserRouter as Router,
  Navigate,
  Routes,
} from "react-router-dom";
import Home from "./Home/components/Home";

function App() {
  return (
    <Router>
      <main>
        <Routes>
          <Route path="/" exact Component={Home} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
