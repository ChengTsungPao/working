import React from 'react';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import Send from './Send/Send'

function UI() {
  return (
    <Router>
      <Route path = "/" component = {Send}/>
    </Router>
  );
}

export default UI;