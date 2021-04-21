import React from 'react';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import Send from './Send/Send'
import Login from './Login/Login'

function UI() {
  return (
    <Router>
      <Route path = "/" exact component = {Login} />
      <Route path = "/Send" component = {Send}/>
    </Router>
  );
}

export default UI;