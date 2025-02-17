import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './HomePage';
import RegisterPage from './RegisterPage';
import ProfilePage from './ProfilePage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage/>} />
        <Route path="/register/:role" element={<RegisterPage/>} />
        <Route path="/profile/:role" element={<ProfilePage/>} />
      </Routes>
    </Router>
  );
};

export default App;
